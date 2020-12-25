import cv2
from constants import *

def draw_rectangle(cv2_image, x, y, width, height, RGB_color, show):
    '''
    Draws a rectangle over given coordinates. Image is shown if shown=True.

    PARAMETERS:
        x = top left x coordinate
        y = top left y coordiante
        width = width of rectangle, in pixels
        height = height of rectangle, in pixels
        RGB_color = tuple color of the outline, e.g. (0, 0, 0)
        show = boolean of whether the image is shown
    '''
    # Draw the rectangle on large_image
    cv2.rectangle(cv2_image, (x, y), (x+width, y+height), RGB_color, 2)
    # Display the original image with the rectangle around the match.
    cv2.imshow('output', cv2_image)
    if show:
        # The image is only displayed if we call this
        cv2.waitKey(0)

def find_identity(cv2_visrep, cv2_target):
    '''
    Uses cv2 image matching to identify the location of a given identity block.

    PARAMETERS:
        cv2_visrep = visrep image file ran through cv2.imread()
        cv2_target = reference image file for the identity block being found ran
            through cv2.imread()
    OUTPUT:
        identity_x = x coordinate of centre of identity block found
        identity_y = y coordinate of centre of identity block found
        start_x = x coordiante starting point for finding chunk size; centre of
            top left quarter of identity block
        start_y = y coordinate of starting point for finding chunk size; centre
            of top left quarter of identity block
    '''
    # Define method for matching
    method = cv2.TM_SQDIFF_NORMED

    # Match images
    result = cv2.matchTemplate(cv2_target, cv2_visrep, method)

    # Find the minimum squared difference
    _, _, match_coord, _ = cv2.minMaxLoc(result)

    # Extract the coordinates of our best match
    match_x, match_y = match_coord

    # Extract the width and height of the target image
    target_width, target_height = cv2_target.shape[:2]

    # Find the centre pixel of the match
    identity_x = int((2*match_x + target_width)/2)
    identity_y = int((2*match_y + target_height)/2)

    # Find reference location for finding chunk size
    # (Center of top left block of identity block)
    start_x = int((4*match_x + target_width)/4)
    start_y = int((4*match_y + target_height)/4)

    draw_rectangle(cv2_visrep, match_x, match_y, target_width, target_height, (0,0,255), False)

    return identity_x, identity_y, start_x, start_y

def check_color_change(cv2_image, x1, y1, x2, y2):
    '''
    Determines whether pixels at two different coordiantes are far enough in
    color (RGB sum difference of each pixel is greater or equal to
    RGB_THRESHOLD) to be considered different colours.

    PARAMETERS:
        cv2_image = image file ran through cv2.imread()
        x1 = x coordinate for first pixel to compare
        y1 = y coordinate for first pixel to compare
        x2 = x coordiante for second pixel to compare
        y2 = y coordinate for second pixel to compare
    OUTPUT:
        If the two pixels are considered different colours, returns True.
        Otherwise, returns False.
    '''
    # If the pixels at (x1, y1) and (x2, y2) are close in brightness
    if abs(sum(list(cv2_image[y1][x1])) - sum(list(cv2_image[y2][x2]))) < RGB_THRESHOLD:
        # Return False
        return False
    # If the pixels are not close enough in brightness, return True
    return True

def find_sizes(start_x, start_y, file_name):
    image = cv2.imread(file_name)

    # Find pixel location to start counting chunk size
    live_x = start_x
    live_y = start_y
    while check_color_change(image, live_x, live_y, live_x-1, live_y) == False:
        live_x += 1

    # Find chunk size
    pixel_count = 1
    while check_color_change(image, live_x, live_y, live_x+1, live_y) == False or pixel_count <= 4:
        live_x += 1
        pixel_count += 1

    chunk_size = (pixel_count)*2

    pixel_count = 1
    live_x += 1
    while check_color_change(image, live_x, live_y, live_x+1, live_y) == False or pixel_count <= 2:
        live_x += 1
        pixel_count += 1
    gap_size = pixel_count

    return chunk_size, gap_size

def check_square_shape(len_top, len_bottom, len_left, len_right):
    '''
    Determins whether a four sided polygon is a square by comparing the lengths
    of the top and the bottom sides, and the left and the right sides.

    PARAMETERS:
        len_top = length of the top side, in pixels
        len_bottom = length of the bottom side, in pixels
        len_left = length of the left side, in pixels
        len_right = length of the right side, in pixels
    OUTPUT:
        If the polygon is considered a square, returns True. Otherwise, returns
        False.
    '''
    proximity_threshold = min([len_top, len_bottom, len_left, len_right])/5
    if (abs(len_top - len_bottom) > proximity_threshold or
        abs(len_left - len_right) > proximity_threshold):
        return False
    return True

def crop_image(cv2_image):
    '''
    Crops a square image. Crops all sides evenly. Intended for identity block
    reference images.
    The reason for cropping is that if the identity block reference images are
    too small or too large for the visrep image being scanned, the identity
    blocks won't be able to be found.

    PARAMETERS:
        cv2_image = image file ran through cv2.imread()
    OUTPUT:
        The provided cv2_image, cropped.
    '''
    length, _, _ = cv2_image.shape
    new_length = int(length*0.9)
    new_length -= new_length%2 # make even number
    padding = int((length - new_length)/2)
    return cv2_image[padding:padding+new_length, padding:padding+new_length]

def scan_visrep(file_name):
    '''
    Scans a given image file's visrep, and returns the 2D matrix representation
    of it.

    PARAMETERS:
        file_name = directory of the image file
    OUTPUT:
        scanned_visrep = 2D matrix (nested lists) representation of the visrep
            found in the given image file
    '''
    image = cv2.imread(file_name)
    scanned_visrep = []

    # Read the images from their file
    target_image1 = cv2.imread(DIR_ID1)
    target_image2 = cv2.imread(DIR_ID2)
    target_image3 = cv2.imread(DIR_ID3)
    target_image4 = cv2.imread(DIR_ID4)
    visrep_image = cv2.imread(file_name)
    while True:
        id1_x, id1_y, start_x, start_y = find_identity(visrep_image, target_image1)
        id2_x, id2_y, _, _ = find_identity(visrep_image, target_image2)
        id3_x, id3_y, _, _ = find_identity(visrep_image, target_image3)
        id4_x, id4_y, _, _ = find_identity(visrep_image, target_image4)

        if check_square_shape(
            len_top=id2_x-id1_x,
            len_bottom=id4_x-id3_x,
            len_left=id3_y-id1_y,
            len_right=id4_y-id2_y):
            break

        target_image1 = crop_image(target_image1)
        target_image2 = crop_image(target_image2)
        target_image3 = crop_image(target_image3)
        target_image4 = crop_image(target_image4)

    chunk_size, gap_size = find_sizes(start_x, start_y, file_name)

    step_size = gap_size + chunk_size

    # Find approximately how many blocks in a row
    approx_block_in_row = int((id4_x - id1_x)/(step_size) + 1)
    # Vertical adjustment due to rotated visreps
    vertical_adjust = int(abs(id1_y - id2_y)/approx_block_in_row)

    live_x = id1_x
    live_y = id1_y + step_size

    def create_block_row(identity_row, live_x, live_y):
        '''
        Creates a list of 0s and 1s which represent one row of the 2D matrix
        which is used to digitally represent a visrep, by detecting whether
        certain pixels are closer to black or white.
        Also updates live_x and live_y's location, which are private variables
        used within the function scan_visrep, of which this function is defined
        in. This makes approximating the centre of the next adjacent block a lot
        more reliable.

        PARAMETERS:
            identity_row = boolean of whether the block row being scanned is
                either one of the top or bottom rows of the visrep, both of
                which hold identity blocks.
            live_x = x coordiante which is adjusted continuously, and is used
                to navigate the visrep and identify the colour at its location
            live_y = y coordinate which is adjusted continuously, and is used
                to navigate the visrep and identify the colour at its location
        OUTPUT:
            block_row = a list of 0s and 1s which represent one row of the 2D
                matrix which is used to digitally represent a visrep
        '''
        block_row = []
        furthest_id_x = max([id2_x, id4_x])
        # Loop through every block in the given row
        if identity_row:
            furthest_id_x -= chunk_size
        while live_x < furthest_id_x+int(chunk_size/2):
            color = list(image[live_y][live_x])

            draw_rectangle(visrep_image, live_x-3, live_y-3, 6, 6, (0,0,255), False)

            # White
            if sum(color) > BRIGHTNESS_THRESHOLD:
                block_row.append(0)
            # Black
            elif sum(color) < BRIGHTNESS_THRESHOLD:
                    block_row.append(1)

            # ADJUST to centre again
            temp_x = live_x
            pixel_count = 0
            visrep_edge = False
            while check_color_change(image, temp_x, live_y, temp_x+1, live_y) == False:
                temp_x += 1
                pixel_count += 1
                if pixel_count > chunk_size:
                    visrep_edge = True
                    break
            adjust_x = int(pixel_count - chunk_size/2)
            if visrep_edge == True:
                adjust_x = 0

            temp_y = live_y
            pixel_count = 0
            visrep_edge = False
            while check_color_change(image, live_x, temp_y, live_x, temp_y+1) == False:
                temp_y += 1
                pixel_count += 1
                if pixel_count > chunk_size:
                    visrep_edge = True
                    break
            adjust_y = int(pixel_count - chunk_size/2)
            if visrep_edge == True:
                adjust_y = 0

            draw_rectangle(visrep_image, live_x-3+adjust_x, live_y-3+adjust_y, 6, 6, (0,255,0), False)

            live_x += step_size + adjust_x
            live_y += vertical_adjust + adjust_y

        return block_row

    # Loop through every row
    while True:
        scanned_visrep.append(create_block_row(False, live_x, live_y))

        live_y += step_size

        if live_y >= id3_y-int(chunk_size/2):
            break

        draw_rectangle(visrep_image, live_x-3, live_y-3, 6, 6, (255,0,0), False)

        temp_y = live_y
        pixel_count = 0
        while check_color_change(image, live_x, temp_y, live_x, temp_y+1) == False:
            temp_y += 1
            pixel_count += 1
        adjust_y = int(pixel_count - chunk_size/2)

        live_y += adjust_y

        temp_x = live_x
        pixel_count = 0
        while check_color_change(image, temp_x, live_y, temp_x+1, live_y) == False:
            temp_x += 1
            pixel_count += 1
        adjust_x = int(pixel_count - chunk_size/2)

        live_x += adjust_x

    live_x = id1_x + step_size
    live_y = id1_y
    scanned_visrep.insert(0, ["I1"] + create_block_row(True, live_x, live_y) + ["I2"])

    live_x = id3_x + step_size
    live_y = id3_y
    scanned_visrep.append(["I3"] + create_block_row(True, live_x, live_y) + ["I4"])

    return scanned_visrep

# Testing
if __name__ == "__main__":
    visrep = scan_visrep('test.png')
    for i in visrep:
        print(i)

    from visrep_to_text import *
    print(decode_visrep(visrep))
