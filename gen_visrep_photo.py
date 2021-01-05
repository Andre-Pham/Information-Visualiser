# Code to generate a visrep png from a visrep 2D matrix

# Import modules
from PIL import Image, ImageDraw
# Import complimenting scripts
from constants import *

def gen_visrep_photo(visrep_matrix, option):
    '''
    Generates and shows a png that represents a visrep via blocks that are
    coloured black and white.

    PARAMETERS:
        visrep_matrix = a 2D matrix (nested lists) that represents text
        option = if option="show", the image is shown to the user, if option is
            a directory, the image is saved to that directory
    '''
    # Define the location for the next block to be drawn
    live_x, live_y = START_X, START_Y
    # Define the png canvas
    canvas = Image.new('RGB', CANVAS_SIZE, color=VISREP_COLOR)
    # Define modification layer of the png canvas
    canvas_draw = ImageDraw.Draw(canvas)

    def draw_block(color):
        '''
        Draws coloured block (square) onto the canvas.
        '''
        # Define coordinates of each corner of the block
        top_left = (live_x, live_y)
        top_right = (live_x + BLOCK_WIDTH, live_y)
        bot_left = (live_x, live_y + BLOCK_WIDTH)
        bot_right = (live_x + BLOCK_WIDTH, live_y + BLOCK_WIDTH)
        # Draw the block onto the canvas
        canvas_draw.polygon(
            [top_left, top_right, bot_right, bot_left],
            fill=color,
            outline=None
        )

    def draw_id_block(id):
        '''
        Draws id block onto canvas.

        PARAMETERS:
            id = if id="I1", draws first id block, if id="I2", draws second id
                block, if id="I3", draws third id block, if id="I4", draws
                fourth id block
        '''
        # Colouring for fourth ID block, I4
        if id == "I4":
            color1 = "white"
            color2 = "black"
        # Colouring for either the first, second or third ID block, I1, I2, I3
        else:
            color1 = "black"
            color2 = "white"

        # Draw full sized block
        draw_block(color1)
        if id != "I2":
            # Draw smaller block in top right of full block
            canvas_draw.polygon(
                [
                    (live_x + BLOCK_WIDTH/2 + 1, live_y),
                    (live_x + BLOCK_WIDTH, live_y),
                    (live_x + BLOCK_WIDTH, live_y + BLOCK_WIDTH/2),
                    (live_x + BLOCK_WIDTH/2 + 1, live_y + BLOCK_WIDTH/2)
                ],
                fill=color2,
                outline=None
            )
        if id != "I3":
            # Draw smaller block in bottom left of full block
            canvas_draw.polygon(
                [
                    (live_x, live_y + BLOCK_WIDTH/2 + 1),
                    (live_x + BLOCK_WIDTH/2, live_y + BLOCK_WIDTH/2 + 1),
                    (live_x + BLOCK_WIDTH/2, live_y + BLOCK_WIDTH),
                    (live_x, live_y + BLOCK_WIDTH)
                ],
                fill=color2,
                outline=None
            )

    # Loop through each row of the visrep_matrix
    for row in visrep_matrix:
        # Loop through each bit of each row
        for bit in row:
            # Draw block, with colour based on bit value
            if bit == 0:
                draw_block("white")
            elif bit == 1:
                draw_block("black")
            else:
                draw_id_block(bit)

            # Adjust x coordinate for next block
            live_x += BLOCK_WIDTH + BLOCK_GAP

        # Adjust the location of the x and y coordinates for the next row to be
        # drawn
        live_x = START_X
        live_y += BLOCK_WIDTH + BLOCK_GAP

    # Display the visrep png
    if option == "show":
        canvas.show()
    else:
        canvas.save(option, "PNG")
