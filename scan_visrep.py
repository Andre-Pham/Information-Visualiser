import cv2
from constants import *

def find_identity(visrep_image, target_image):
    # Define method for matching
    method = cv2.TM_SQDIFF_NORMED

    '''
    # Read the images from their file
    target_image = cv2.imread(target_png)
    visrep_image = cv2.imread(file_name)
    '''

    # Match images
    result = cv2.matchTemplate(target_image, visrep_image, method)

    # Find the minimum squared difference
    _, _, match_coord, _ = cv2.minMaxLoc(result)

    # Extract the coordinates of our best match
    match_x, match_y = match_coord

    # Extract the width and height of the target image
    target_width, target_height = target_image.shape[:2]

    # Find the centre pixel of the match
    identity_x = int((2*match_x + target_width)/2)
    identity_y = int((2*match_y + target_height)/2)

    # Find reference location for finding chunk size
    # (Center of top left block of identity block)
    start_x = int((4*match_x + target_width)/4)
    start_y = int((4*match_y + target_height)/4)

    #print(target_png)
    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(visrep_image, (match_x, match_y), (match_x+target_width, match_y+target_height), (0,0,255), 2)
    # Display the original image with the rectangle around the match.
    cv2.imshow('output',visrep_image)
    # The image is only displayed if we call this
    cv2.waitKey(0)

    return identity_x, identity_y, start_x, start_y

def find_sizes(start_x, start_y, file_name):
    image = cv2.imread(file_name)

    def check_color_change(x1, y1, x2, y2):
        # If the pixels at (x1, y1) and (x2, y2) are close in brightness
        if abs(sum(list(image[y1][x1])) - sum(list(image[y2][x2]))) < RGB_THRESHOLD:
            # Return False
            return False
        # If the pixels are not close enough in brightness, return True
        return True

    # Find pixel location to start counting chunk size
    live_x = start_x
    live_y = start_y
    while check_color_change(live_x, live_y, live_x-1, live_y) == False:
        live_x += 1

    # Because of soft edges, just to be safe
    #SAFETY_NET = 1
    live_x# += SAFETY_NET

    # Find chunk size
    pixel_count = 1
    while check_color_change(live_x, live_y, live_x+1, live_y) == False:
        live_x += 1
        pixel_count += 1

    chunk_size = (pixel_count)*2

    # Find gap size via ratios
    '''ADJUST THIS WHEN constants.py BLOCK_GAP and BLOCK_WIDTH are fixed; remove "- 1" and "+ 1".'''
    gap_size = int((BLOCK_GAP - 1)/(BLOCK_WIDTH + 1) * chunk_size)

    return chunk_size, gap_size

def check_square_shape(top, bottom, left, right):
    '''
    Top, bottom, left and right are the lengths of the square.
    '''
    proximity_threshold = min([top, bottom, left, right])/5
    print(proximity_threshold)
    print(top, bottom, left, right)
    print('------------------')
    if (abs(top - bottom) > proximity_threshold or
        abs(left - right) > proximity_threshold):
        return False
    return True

def crop_image(image):
    length, _, _ = image.shape
    new_length = int(length*0.9)
    new_length -= new_length%2 # make even number
    padding = int((length - new_length)/2)
    return image[padding:padding+new_length, padding:padding+new_length]

def scan_visrep(file_name):
    image = cv2.imread(file_name)
    scanned_visrep = []

    # Read the images from their file
    target_image1 = cv2.imread("identity1.png")
    target_image2 = cv2.imread("identity2.png")
    target_image3 = cv2.imread("identity3.png")
    target_image4 = cv2.imread("identity4.png")
    visrep_image = cv2.imread(file_name)
    while True:
        id1_x, id1_y, start_x, start_y = find_identity(visrep_image, target_image1)
        id2_x, id2_y, _, _ = find_identity(visrep_image, target_image2)
        id3_x, id3_y, _, _ = find_identity(visrep_image, target_image3)
        id4_x, id4_y, _, _ = find_identity(visrep_image, target_image4)

        if check_square_shape(id2_x-id1_x, id4_x-id3_x, id3_y-id1_y, id4_y-id2_y):
            break
        else:
            target_image1 = crop_image(target_image1)
            target_image2 = crop_image(target_image2)
            target_image3 = crop_image(target_image3)
            target_image4 = crop_image(target_image4)

    chunk_size, gap_size = find_sizes(start_x, start_y, file_name)

    step_size = gap_size + chunk_size

    #find how many blocks in a row
    block_in_row = int((id4_x - id1_x)/(step_size) + 1)
    # Vertical adjustment due to rotated visreps
    vertical_adjust = int(abs(id1_y - id2_y)/block_in_row)

    print_statment = \
    f'''
    chunk_size (block length) = {chunk_size}
    gap_size = {gap_size}
    block_in_row = {block_in_row}
    vertical_adjust = {vertical_adjust}
    '''
    print(print_statment)

    live_x = id1_x
    live_y = id1_y + step_size

    def create_block_row(range_values, live_x, live_y):
        block_row = []
        # Loop through every block in the given row
        for _ in range(range_values):
            color = list(image[live_y][live_x])

            #print(target_png)
            # Step 3: Draw the rectangle on large_image
            cv2.rectangle(visrep_image, (live_x-3, live_y-3), (live_x+3, live_y+3), (0,0,255), 2)
            # Display the original image with the rectangle around the match.
            cv2.imshow('output',visrep_image)
            # The image is only displayed if we call this
            cv2.waitKey(0)

            # White
            if sum(color) > BRIGHTNESS_THRESHOLD:
                block_row.append(0)
            # Black
            elif sum(color) < BRIGHTNESS_THRESHOLD:
                    block_row.append(1)
            # Error detector
            else:
                print("ERROR DETECTED: NO BLACK OR WHITE FOUND")
                scanned_visrep.append("ERROR")
            live_x += step_size
            live_y += vertical_adjust
        return block_row

    # Loop through every row
    for _ in range(block_in_row-2):
        scanned_visrep.append(create_block_row(block_in_row, live_x, live_y))
        live_y += step_size

    live_x = id1_x + step_size
    live_y = id1_y
    scanned_visrep.insert(0, ["I1"] + create_block_row(block_in_row-2, live_x, live_y) + ["I2"])

    live_x = id1_x + step_size
    live_y = id1_y + step_size*(block_in_row - 1)
    scanned_visrep.append(["I3"] + create_block_row(block_in_row-2, live_x, live_y) + ["I4"])

    return scanned_visrep

# Testing
if __name__ == "__main__":
    visrep = scan_visrep('test.png')
    for i in visrep:
        print(i)

    from visrep_to_text import *
    print(decode_visrep(visrep))
