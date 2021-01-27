# Code to generate text from visual representation photos

# Import modules
import cv2
from PIL import Image, ImageEnhance, ImageStat
import numpy as np
# Import complimenting scripts
from constants import *

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
    # Calculate proximity_threshold, which is an abstract value which is the
    # minimum value that the top/bottom and left/right lengths can be
    # different by for the polygon to still be considered a square.
    proximity_threshold = min([len_top, len_bottom, len_left, len_right])/5

    # If the top length and bottom length difference, or the left and right
    # length difference is greater than the proximity threshold
    if (abs(len_top - len_bottom) > proximity_threshold or
        abs(len_left - len_right) > proximity_threshold):
        # The polygon is not a square
        return False
    # Otherwise, the polygon is a square
    return True

def expand_image(cv2_image):
    '''
    Expands a square image. Expands all sides evenly. Intended for identity
    block reference images.
    The reason for expanding is that if the identity block reference images are
    too small or too large for the visrep image being scanned, the identity
    blocks won't be able to be found.

    PARAMETERS:
        cv2_image = image file ran through cv2.imread()
    OUTPUT:
        The provided cv2_image, expanded.
    '''
    # Determine the length (width and height = length because image is square)
    length, _, _ = cv2_image.shape
    # Determine the new length
    if length >= ID_RESIZE_COMPOUND_THRESHOLD:
        new_length = int(length*ID_RESIZE_COMPOUND)
        # Make new_length an even number so there's equal black/white pixels
        new_length -= new_length%2
    else:
        new_length = length + ID_RESIZE_INCREMENT
    # Expand the image
    cv2_image = cv2.resize(
        cv2_image,
        (new_length, new_length),
        interpolation = cv2.INTER_NEAREST
    )
    # Return the expanded image
    return cv2_image

def read_visrep_photo(file_dir):
    '''
    Scans a given image file's visrep, and returns the 2D matrix representation
    of it.

    PARAMETERS:
        file_dir = directory of the image file to be converted to a 2D matrix
            representation, or a cv2 read visrep image (both work)
    OUTPUT:
        visrep_matrix = 2D matrix (nested lists) representation of the visrep
            found in the given image file
    '''
    if type(file_dir) == str:
        # Read the image using cv2
        cv2_visrep = cv2.imread(file_dir)
    else:
        # Define the cv2 image
        cv2_visrep = file_dir

    # Identify the height and width of the visrep
    height, width, _ = cv2_visrep.shape
    # Identify the longest side of the visrep
    max_length = max([width, height])
    # If the visrep is too large, resize the visrep
    if max_length > MAX_LENGTH:
        scale = MAX_LENGTH/max_length
        new_width = int(width*scale)
        new_height = int(height*scale)
        cv2_visrep = cv2.resize(
            cv2_visrep,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    def find_identity(cv2_target, method):
        '''
        Uses cv2 image matching to identify the location of a given identity
        block.

        PARAMETERS:
            cv2_target = reference image file for the identity block being found
                ran through cv2.imread()
        OUTPUT:
            identity_x = x coordinate of centre of identity block found
            identity_y = y coordinate of centre of identity block found
            start_x = x coordiante starting point for finding chunk size; centre
                of top left quarter of identity block
            start_y = y coordinate of starting point for finding chunk size;
                centre of top left quarter of identity block
        '''
        nonlocal cv2_visrep

        # Define the width and height of the target image
        target_width, target_height = cv2_target.shape[:2]

        # Match images
        result = cv2.matchTemplate(cv2_target, cv2_visrep, method)

        # Find the minimum squared difference coordinates
        _, _, match_coord, _ = cv2.minMaxLoc(result)
        # Extract the coordinates of our best match
        match_x, match_y = match_coord

        # Find the centre pixel of the match
        identity_x = int((2*match_x + target_width)/2)
        identity_y = int((2*match_y + target_height)/2)

        # Find reference location for finding chunk size
        # (Center of top left block of identity block)
        start_x = int((4*match_x + target_width)/4)
        start_y = int((4*match_y + target_height)/4)

        return identity_x, identity_y, start_x, start_y

    # Define the final 2D matrix to be returned
    visrep_matrix = []

    # Read the reference identity images from their file
    target_image1 = cv2.imread(DIR_ID1)
    target_image2 = cv2.imread(DIR_ID2)
    target_image3 = cv2.imread(DIR_ID3)
    target_image4 = cv2.imread(DIR_ID4)
    # Define the false reference identity images
    false_target1 = cv2.rotate(target_image2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    false_target2 = cv2.rotate(target_image3, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Define method for matching images
    method = cv2.TM_SQDIFF_NORMED
    # Define the minimum length of the visrep image
    cv2_visrep_min_length = min([cv2_visrep.shape[0], cv2_visrep.shape[1]])
    # Define rotation required for correct orientation
    rotation = None
    # This loop continuously defines the identity block locations, checks if
    # they form a valid square, crops the images if they aren't a valid
    # square, then repeats the process
    while True:
        # Define the centre (id#_x, id#_y) of each identity block, as well
        # as start_x and start_y, which are the starting points for finding
        # the gap size and chunk size
        id1_x, id1_y, start_x, start_y = find_identity(target_image1, method)
        id2_x, id2_y, _, _ = find_identity(target_image2, method)
        id3_x, id3_y, _, _ = find_identity(target_image3, method)
        id4_x, id4_y, _, _ = find_identity(target_image4, method)

        # Define the position of the false identity blocks
        fid1_x, fid1_y, _, _ = find_identity(false_target1, method)
        fid2_x, fid2_y, _, _ = find_identity(false_target2, method)

        # If visrep is rotated 90 degrees
        if (check_square_shape(
                len_top=id4_x-fid1_x,
                len_bottom=fid2_x-id1_x,
                len_left=id1_y-fid1_y,
                len_right=fid2_y-id4_y) and
                # Top left diagonal to bottom right
                fid1_x < fid2_x and fid1_y < fid2_y and
                # Bottom left diagonal to top right
                id1_x < id4_x and id1_y > id4_y):
            rotation = cv2.ROTATE_90_COUNTERCLOCKWISE
            cv2_visrep = cv2.rotate(cv2_visrep, rotation)
            continue
        # If visrep is rotated 180 degrees
        if (check_square_shape(
                len_top=id2_x-id4_x,
                len_bottom=id1_x-id3_x,
                len_left=id3_y-id4_y,
                len_right=id1_y-id2_y) and
                # Top left diagonal to bottom right
                id4_x < id1_x and id4_y < id1_y and
                # Bottom left diagonal to top right
                id3_x < id2_x and id3_y > id2_y):
            rotation = cv2.ROTATE_180
            cv2_visrep = cv2.rotate(cv2_visrep, rotation)
            continue
        # If visrep is rotated -90 degrees
        if (check_square_shape(
                len_top=id1_x-fid1_x,
                len_bottom=fid2_x-id4_x,
                len_left=id4_y-fid1_y,
                len_right=fid2_y-id1_y) and
                # Top left diagonal to bottom right
                fid1_x < fid2_x and fid1_y < fid2_y and
                # Bottom left diagonal to top right
                id4_x < id1_x and id4_y > id1_y):
            rotation = cv2.cv2.ROTATE_90_CLOCKWISE
            cv2_visrep = cv2.rotate(cv2_visrep, rotation)
            continue

        # Determines if the defined positions of the identity blocks form a
        # square (and hence the identity block locations found are valid)
        if check_square_shape(
                len_top=id2_x-id1_x,
                len_bottom=id4_x-id3_x,
                len_left=id3_y-id1_y,
                len_right=id4_y-id2_y):
            # Stop searching for identity blocks
            break

        # If the identity block locations aren't valid, expand the refernce
        # identity block images
        # (this is due to cv2 struggling to find matching images if their
        # sizes are different)
        target_image1 = expand_image(target_image1)
        # If the identity blocks can't be found
        if target_image1.shape[0] > 60 and method == cv2.TM_SQDIFF_NORMED:
            # Use a different matching method
            target_image1 = cv2.imread(DIR_ID1)
            target_image2 = cv2.imread(DIR_ID2)
            target_image3 = cv2.imread(DIR_ID3)
            target_image4 = cv2.imread(DIR_ID4)
            false_target1 = cv2.rotate(target_image2, cv2.ROTATE_90_COUNTERCLOCKWISE)
            false_target2 = cv2.rotate(target_image3, cv2.ROTATE_90_COUNTERCLOCKWISE)
            method = cv2.TM_SQDIFF
            continue
        # If the identity blocks still can't be found
        if target_image1.shape[0] > cv2_visrep_min_length/10:
            # Give up searching
            raise Exception("No identity blocks found")
        target_image2 = expand_image(target_image2)
        target_image3 = expand_image(target_image3)
        target_image4 = expand_image(target_image4)
        false_target1 = expand_image(false_target1)
        false_target2 = expand_image(false_target2)

    if type(file_dir) == str:
        # Read the visrep using PIL
        PIL_visrep = Image.open(file_dir)
    else:
        # If cv2 image is provided, convert provided cv2 image to PIL image
        frame_convert = cv2.cvtColor(file_dir, cv2.COLOR_BGR2RGB)
        PIL_visrep = Image.fromarray(frame_convert)
    # Identify the brightness adjustment
    # 1. Identify four known black pixels (next to each other)
    black_color_ref_list = [
        sum(list(cv2_visrep[start_y-1][start_x-1])),
        sum(list(cv2_visrep[start_y-1][start_x])),
        sum(list(cv2_visrep[start_y][start_x])),
        sum(list(cv2_visrep[start_y][start_x-1]))
    ]
    # 2. Average the BGR colour value to estimate the average black pixel colour
    black_color_ref = sum(black_color_ref_list)/4
    # 3. Determine the amount of brightness adjustment needed relative to how
    # bright the estimated average black pixel is
    # (based on fitted cubic graph using points [0, 1.7], [52, 1.6],
    # [164.5, 1.2], [381, 0.7] which were collected from testing images)
    brightness_enhance = (
        3.5988E-8*black_color_ref**3 -
        1.7715E-5*black_color_ref**2 -
        1.0992E-3*black_color_ref +
        1.7000
    )
    # Enhance the brightness
    enhancer = ImageEnhance.Brightness(PIL_visrep)
    PIL_visrep_enhance = enhancer.enhance(brightness_enhance)
    # Identify contrast adjustment
    # (based on fitted cubic graph using points [0, 1], [52, 1.3], [164.5, 1.5],
    # [381, 2] which were collected from testing images)
    contrast_enhance = (
        6.7927E-08*black_color_ref**3 -
        3.8970E-05*black_color_ref**2 +
        7.6120E-03*black_color_ref +
        1.0000
    )
    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(PIL_visrep_enhance)
    PIL_visrep_enhance = enhancer.enhance(contrast_enhance)

    # Convert the enhanced PIL visrep to cv2
    cv2_visrep_enhance = cv2.cvtColor(
        np.array(PIL_visrep_enhance),
        cv2.COLOR_RGB2BGR
    )
    # If the visrep is too large, resize the visrep
    if max_length > MAX_LENGTH:
        cv2_visrep_enhance = cv2.resize(
            cv2_visrep_enhance,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )
    # If the visrep is the incorrect orientation, rotate the image
    if rotation != None:
        cv2_visrep_enhance = cv2.rotate(cv2_visrep_enhance, rotation)

    def check_color_change(x1, y1, x2, y2):
        '''
        Determines whether pixels at two different coordiantes are far enough in
        color (BGR sum difference of each pixel is greater or equal to
        BGR_THRESHOLD) to be considered different colours.

        PARAMETERS:
            x1 = x coordinate for first pixel to compare
            y1 = y coordinate for first pixel to compare
            x2 = x coordiante for second pixel to compare
            y2 = y coordinate for second pixel to compare
        OUTPUT:
            If the two pixels are considered different colours, returns True.
            Otherwise, returns False.
        '''
        nonlocal cv2_visrep_enhance

        # Define BGR colours of the two pixels being compared
        bgr1 = list(cv2_visrep_enhance[y1][x1])
        bgr2 = list(cv2_visrep_enhance[y2][x2])

        # If the pixels at (x1, y1) and (x2, y2) are not close in brightness
        if (abs(sum(bgr1) - sum(bgr2)) >= BGR_THRESHOLD and
                # If the image blacks are too bright, detecting by brightness
                # is not reliable because same-colour pixels will have great
                # contrast, hence the 'and black_color_ref' requirement
                black_color_ref < 300 or
                # Or the blue channels are far apart enough
                abs(int(bgr1[0]) - int(bgr2[0])) >= BGR_CHANNEL_THRESHOLD or
                # Or the green channels are far apart enough
                abs(int(bgr1[1]) - int(bgr2[1])) >= BGR_CHANNEL_THRESHOLD or
                # Or the red channels are far apart enough
                abs(int(bgr1[2]) - int(bgr2[2])) >= BGR_CHANNEL_THRESHOLD):
            # Return True
            return True
        # If the pixels are close enough in brightness, return False
        return False

    def find_largest_contrast(coord1, coord2, coord3, coord4):
        '''
        Determines which two adjacent pixels have the greatest contrast, out of
        four given coordinates.

        PARAMETERS:
            coord1 = (x, y) coordinates in list form
            coord2 = (x, y) coordinates in list form, between coord1 and coord3
            coord3 = (x, y) coordinates in list form, between coord2, and coord4
            coord4 = (x, y) coordinates in list form, after coord3
        OUTPUT:
            x = the x coordinate of the highest contrast pixel, relative to its
                adjacent pixel (of the two pixels with the highest contrast, x
                favoures the one on the right)
            y = the y coordinate of the highest contrast pixel, relative to its
                adjacent pixel (of the two pixels with the highest contrast, y
                favours the one on the bottom)
            pixel_count_add_x = how many pixels difference between the given x
                coordinate and the pixel with the highest contrast (of the two
                pixels with the highest contrast, favours the one on the left)
            pixel_count_add_y = how many pixels difference between the given y
                coordiante and the pixel with the highest contrast (of the two
                pixels with the highest contrast, favours the one on the top)
        '''
        nonlocal cv2_visrep_enhance

        # Define the colour values of each coordinate
        coord1_color = sum(list(cv2_visrep_enhance[coord1[1]][coord1[0]]))
        coord2_color = sum(list(cv2_visrep_enhance[coord2[1]][coord2[0]]))
        coord3_color = sum(list(cv2_visrep_enhance[coord3[1]][coord3[0]]))
        coord4_color = sum(list(cv2_visrep_enhance[coord4[1]][coord4[0]]))

        # Define a list of all the contrasts between the adjacent pixels
        contrasts = [
            abs(coord1_color - coord2_color),
            abs(coord2_color - coord3_color),
            abs(coord3_color - coord4_color)
        ]

        # Identify the index of the two pixels with the highest contrast
        max_contrast_pos = contrasts.index(max(contrasts))

        # Identify the coordinate with the highest contrast (favoured right)
        x, y = [coord2, coord3, coord4][max_contrast_pos]

        # Identify the distance between the original coordaintes and the highest
        # contrast coordinate (favoured left, hence the '- 1')
        pixel_count_add_x = x - coord1[0] - 1
        pixel_count_add_y = y - coord1[1] - 1

        return x, y, pixel_count_add_x, pixel_count_add_y

    def find_sizes(start_x, start_y):
        '''
        Identifies the length of the blocks in the visrep, as well as the gap
        between the blocks in the visrep, which are critical to measuring out
        the rest of the visrep.

        PARAMETERS:
            start_x = x coordiante starting point for finding chunk size; centre
                of top left quarter of identity block
            start_y = y coordinate of starting point for finding chunk size;
                centre of top left quarter of identity block
        OUTPUT:
            block_len = length of the blocks in the visrep, in pixels
            gap_size = length of the gap between the blocks in the visrep, in
                pixels
        '''
        live_x = start_x
        live_y = start_y

        # Find pixel location to start counting chunk size by moving pixel by
        # pixel right until the next pixel is a different colour
        while not check_color_change(live_x, live_y, live_x+3, live_y):
            live_x += 1
        live_x, live_y, _, _ = find_largest_contrast(
            [live_x, live_y],
            [live_x+1, live_y],
            [live_x+2, live_y],
            [live_x+3, live_y]
        )

        # Find length of the top right quarter of the top left identity block by
        # moving pixel by pixel right until the next pixel is a different colour
        # (must be <= 2, to avoid detecting soft edges as colour changes)
        # 1. Find a pixel where three pixels to the right, theres a colour
        # change
        pixel_count = 1
        while (not check_color_change(live_x, live_y, live_x+3, live_y) or
                pixel_count <= 2):
            live_x += 1
            pixel_count += 1
        # 2. Of the four pixels representing a colour change, identify the two
        # pixels with the most contrast, and update pixel_count, live_x and
        # live_y
        live_x, live_y, pixel_count_add_x, _ = find_largest_contrast(
            [live_x, live_y],
            [live_x+1, live_y],
            [live_x+2, live_y],
            [live_x+3, live_y]
        )
        pixel_count += pixel_count_add_x
        # Calculate chunk size
        block_len = (pixel_count)*2

        # Find gap length by moving pixel by pixel right until there is a colour
        # change (must be <= 2, to avoid detecting soft edges as colour changes)
        pixel_count = 1
        # 1. Find a pixel where three pixels to the right, theres a colour
        # change
        while (not check_color_change(live_x, live_y, live_x+3, live_y) or
               pixel_count <= 2):
            live_x += 1
            pixel_count += 1
        # 2. Of the four pixels representing a colour change, identify the
        # pixels with the most contrast, and update pixel_count, live_x and
        # live_y
        live_x, live_y, pixel_count_add_x, _ = find_largest_contrast(
            [live_x, live_y],
            [live_x+1, live_y],
            [live_x+2, live_y],
            [live_x+3, live_y]
        )
        pixel_count += pixel_count_add_x
        # Determine gap size
        gap_size = pixel_count

        return block_len, gap_size

    # Calculate chunk size and gap size
    block_len, gap_size = find_sizes(start_x, start_y)
    # Define the step size
    step_size = gap_size + block_len

    # Find approximately how many blocks in a row
    approx_block_in_row = int((id4_x - id1_x)/(step_size) + 1)
    # Vertical adjustment (applied to each new block) due to rotated visreps
    vertical_adjust = int(abs(id1_y - id2_y)/approx_block_in_row)

    def create_block_row(identity_row, live_x, live_y):
        '''
        Creates a list of 0s and 1s which represent one row of the 2D matrix
        which is used to digitally represent a visrep, by detecting whether
        certain pixels are closer to black or white.
        Also updates live_x and live_y's location, which are private
        variables used within the function read_visrep_photo, of which this
        function is defined in. This makes approximating the centre of the
        next adjacent block a lot more reliable.

        PARAMETERS:
            identity_row = boolean of whether the block row being scanned is
                either one of the top or bottom rows of the visrep, both of
                which hold identity blocks.
            live_x = x coordiante which is adjusted continuously, and is
                used to navigate the visrep and identify the colour at its
                location
            live_y = y coordinate which is adjusted continuously, and is
                used to navigate the visrep and identify the colour at its
                location
        OUTPUT:
            block_row = a list of 0s and 1s which represent one row of the
                2D matrix which is used to digitally represent a visrep
        '''
        # Define the block row to be returned
        block_row = []

        # If it's the top identity row
        if identity_row == "TOP":
            # The furthest x coordinate allowed is to the left of the identity
            x_limit = id2_x - int(block_len/2)
        # If it's the bottom identity row
        elif identity_row == "BOTTOM":
            # The furthest x coordinate allowed is to the left of the identity
            x_limit = id4_x - int(block_len/2)
        # If it's not an identity row
        else:
            # Calculate the right side x coordinate of the visrep for this row
            # (x_limit)
            right_ids_height_diff = id4_y - id2_y
            right_ids_width_diff = id4_x - id2_x
            distance_down = live_y - id2_y
            x_limit = int(
                id2_x +
                right_ids_width_diff*distance_down/right_ids_height_diff +
                block_len/2
            )

        # Loop until live_x reaches further than the visrep's side
        while live_x < x_limit:
            # Determine the colour at the current live coordinates
            # (first block)
            color = list(cv2_visrep_enhance[live_y][live_x])

            # If the colour is bright, assume white, and add it to the block
            # row
            if sum(color) > BRIGHTNESS_THRESHOLD:
                block_row.append(0)
            # If the colour is dark, assume black, and add it to the block
            # row
            elif sum(color) < BRIGHTNESS_THRESHOLD:
                block_row.append(1)

            # Calculate the amount of adjustment needed for live_x to be in
            # the horizontal centre of the block it's in
            temp_x = live_x
            pixel_count = 0
            visrep_edge = False
            # 1. Detect how many pixels of similar-enough colour there is to
            # the right
            while not check_color_change(temp_x, live_y, temp_x+3, live_y):
                temp_x += 1
                pixel_count += 1
                # If there are more similarly-coloured pixels to the right
                # than the size of an entire chunk, either something's
                # wrong, or we've reached the end of the visrep
                # (and black/white just continues)
                if pixel_count > block_len:
                    visrep_edge = True
                    break
            _, _, pixel_count_add_x, _ = find_largest_contrast(
                [temp_x, live_y],
                [temp_x+1, live_y],
                [temp_x+2, live_y],
                [temp_x+3, live_y]
            )
            pixel_count += pixel_count_add_x
            # 2. Calculate the amount of adjustment needed, which is the
            # difference between the pixels counted, and the expected amount
            # of pixels
            adjust_x = int(pixel_count - block_len/2)
            # 3. If the edge was detected, no adjustment is needed
            if visrep_edge == True:
                adjust_x = 0

            # Calculate the amount of adjustment needed for live_y to be in
            # the vertical centre of the block it's in
            temp_y = live_y
            pixel_count = 0
            visrep_edge = False
            # 1. Detect how many pixels of similar-enough colour there is
            # downwards
            while not check_color_change(live_x, temp_y, live_x, temp_y+3):
                temp_y += 1
                pixel_count += 1
                # If there are more similarly-coloured pixels downwards than
                # the size of an entire chunk, either something's wrong, or
                # we've reached the end of the visrep (and black/white just
                # continues)
                if pixel_count > block_len:
                    visrep_edge = True
                    break
            _, _, _, pixel_count_add_y = find_largest_contrast(
                [live_x, temp_y],
                [live_x, temp_y+1],
                [live_x, temp_y+2],
                [live_x, temp_y+3]
            )
            pixel_count += pixel_count_add_y
            # 2. Calculate the amount of adjustment needed, which is the
            # difference between the pixels counted, and the expected amount
            # of pixels
            adjust_y = int(pixel_count - block_len/2)
            # 3. If the edge was detected, no adjustment is needed
            if visrep_edge == True:
                adjust_y = 0

            # Adjust live_x to the horizontal centre of the block which was
            # just read
            live_x += step_size + adjust_x
            # Adjust live_y to the vertical centre of the block which was
            # just read
            live_y += vertical_adjust + adjust_y

        return block_row

    # Define live_x and live_y, which are coordinates which continuously
    # change to determine the colour of different pixels at different
    # locations (start at the centre of the first block's location)
    live_x = id1_x
    live_y = id1_y + step_size

    # This loop generates block rows for every row between the identity rows
    while True:
        # Generate and append the block row for the current live x and y
        visrep_matrix.append(create_block_row(False, live_x, live_y))

        # Increase live_y by a block, to move to the next row
        live_y += step_size

        # If live_y is passed the top of the third identity block, there are
        # no more rows to add, so the loop is broken
        if live_y >= id3_y-int(block_len/2):
            break

        # Adjust live_x to the horizontal centre of the block which was
        # just read (the starting block of the new row to be scanned)
        temp_x = live_x
        pixel_count = 0
        while not check_color_change(temp_x, live_y, temp_x+3, live_y):
            temp_x += 1
            pixel_count += 1
        _, _, pixel_count_add_x, _ = find_largest_contrast(
            [temp_x, live_y],
            [temp_x+1, live_y],
            [temp_x+2, live_y],
            [temp_x+3, live_y]
        )
        pixel_count += pixel_count_add_x
        adjust_x = int(pixel_count - block_len/2)
        # Only adjust x if the adjustment is smaller than a block length to
        # avoid errors of over-correction
        if adjust_x < block_len:
            live_x += adjust_x

        # Adjust live_y to the vertical centre of the block which was just
        # read (the starting block of the new row to be scanned)
        temp_y = live_y
        pixel_count = 0
        while not check_color_change(live_x, temp_y, live_x, temp_y+1):
            temp_y += 1
            pixel_count += 1
        _, _, _, pixel_count_add_y = find_largest_contrast(
            [live_x, temp_y],
            [live_x, temp_y+1],
            [live_x, temp_y+2],
            [live_x, temp_y+3]
        )
        pixel_count += pixel_count_add_y
        adjust_y = int(pixel_count - block_len/2)
        # Only adjust y if the adjustment is smaller than a block length to
        # avoid errors of over-correction
        if adjust_y < block_len:
            live_y += adjust_y

    # Redefine live x and y to be at the estimated centre of the first block
    # of the top identity row
    live_x = id1_x + step_size
    live_y = id1_y
    # Generate and append the top identity block row
    visrep_matrix.insert(
        0,
        ["I1"] + create_block_row("TOP", live_x, live_y) + ["I2"]
    )

    # Redefine live x and y to be at the estimated centre of the first block
    # of the bottom identity row
    live_x = id3_x + step_size
    live_y = id3_y
    # Generate and append the bottom identity block row
    visrep_matrix.append(
        ["I3"] + create_block_row("BOTTOM", live_x, live_y) + ["I4"]
    )

    return visrep_matrix
