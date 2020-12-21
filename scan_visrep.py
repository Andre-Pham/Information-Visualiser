import cv2
from constants import *

def find_identity_start(file_name):

    method = cv2.TM_SQDIFF_NORMED

    # Read the images from the file
    small_image = cv2.imread('identity_start.png')
    large_image = cv2.imread(file_name)

    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]

    return (MPx+1, MPy+1)

def find_identity_end(file_name):
    method = cv2.TM_SQDIFF_NORMED

    # Read the images from the file
    small_image = cv2.imread('identity_end.png')
    large_image = cv2.imread(file_name)

    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc

    return (MPx+1, MPy+1)

def find_sizes(start_x, start_y, end_x, end_y, file_name):
    image = cv2.imread(file_name)

    #find chunk size
    pixel_count = 0
    x = start_x + 1
    #find chunck size
    while list(image[x][start_y]) == [255, 255, 255]:
        pixel_count += 1
        x += 1

    chunk_size = pixel_count*2

    #find gap size
    pixel_count = 0
    while list(image[x][start_y]) not in [[255, 255, 255], [0, 0, 0]]:
        pixel_count += 1
        x += 1

    gap_size = pixel_count
    return chunk_size, gap_size
    '''
    #for ratio method
    gap_size = BLOCK_GAP/BLOCK_WIDTH * chunk_size

    return chunk_size,int(gap_size)
    '''

def scan_visrep(file_name):
    image = cv2.imread(file_name)
    scanned_visrep = []
    start_x, start_y = find_identity_start(file_name)
    end_x, end_y = find_identity_end(file_name)
    chunk_size, gap_size = find_sizes(start_x, start_y, end_x, end_y, file_name)

    step_size = gap_size + chunk_size

    live_x = start_x
    live_y = start_y

    #find how many blocks in a row
    block_in_row = int((end_x - start_x)/(step_size) + 1)

    for row in range(block_in_row-2):
        for block in range(block_in_row):
            live_step = block*step_size
            scanned_visrep.append(list(image[live_x+step_size*row][live_y+live_step]))

    print(scanned_visrep)

scan_visrep('test.png')

'''
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
black = 0
white = 225

purple = 205
'''
