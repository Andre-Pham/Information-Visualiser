# Code to generate a visrep png from a visrep 2D matrix

# Import modules
from PIL import Image, ImageDraw
# Import complimenting scripts
from constants import *

def generate_visrep_png(visrep, option):
    '''
    Generates and shows a png that represents a visrep via blocks that are
    coloured black and white.
    Option is a string. If option == "show", the image is shown as a png. If
    option is a directory, the image is saved to that directory.
    '''
    # Define the location for the next block to be drawn
    live_x, live_y = START_X, START_Y
    # Define the png canvas
    canvas = Image.new('RGB', CANVAS_SIZE, color=BACKGROUND_COLOR)
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
        If parameter id="I1", draws first id block with black squares "pointing"
        to centre.
        If parameter id="I2", draws second id block with black squares
        "pointing" perpendicular to centre.
        '''
        # Colouring for first ID block, I1
        if id == "I1":
            color1 = "white"
            color2 = "black"
        # Colouring for second ID block, I2
        else:
            color1 = "black"
            color2 = "white"

        # Draw full sized block
        draw_block(color1)
        # Draw smaller block in top left of full block
        canvas_draw.polygon(
            [
                (live_x, live_y),
                (live_x + BLOCK_WIDTH/2, live_y),
                (live_x + BLOCK_WIDTH/2, live_y + BLOCK_WIDTH/2),
                (live_x, live_y + BLOCK_WIDTH/2)
            ],
            fill=color2,
            outline=None
        )
        # Draw smaller block in top right of full block
        canvas_draw.polygon(
            [
                (live_x + BLOCK_WIDTH/2 + 1, live_y + BLOCK_WIDTH/2 + 1),
                (live_x + BLOCK_WIDTH, live_y + BLOCK_WIDTH/2 + 1),
                (live_x + BLOCK_WIDTH, live_y + BLOCK_WIDTH),
                (live_x + BLOCK_WIDTH/2 + 1, live_y + BLOCK_WIDTH)
            ],
            fill=color2,
            outline=None
        )

    # Loop through each row of the visrep
    for row in visrep:
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
