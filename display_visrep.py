# Code to generate a visrep png from a visrep 2D matrix

# Import modules
from PIL import Image, ImageDraw
# Import complimenting scripts
from constants import *

def generate_visrep_png(visrep):
    '''
    Generates and shows a png that represents a visrep via blocks that are
    coloured black and white.
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

    def draw_id_block(id_x, id_y):
        canvas_draw.polygon(
            [
                (id_x, id_y),
                (id_x + BLOCK_WIDTH, id_y),
                (id_x + BLOCK_WIDTH, id_y + BLOCK_WIDTH),
                (id_x, id_y + BLOCK_WIDTH)
            ],
            fill="white",
            outline=None
        )
        canvas_draw.polygon(
            [
                (id_x, id_y),
                (id_x + BLOCK_WIDTH/2, id_y),
                (id_x + BLOCK_WIDTH/2, id_y + BLOCK_WIDTH/2),
                (id_x, id_y + BLOCK_WIDTH/2)
            ],
            fill="black",
            outline=None
        )
        canvas_draw.polygon(
            [
                (id_x + BLOCK_WIDTH/2 + 1, id_y + BLOCK_WIDTH/2 + 1),
                (id_x + BLOCK_WIDTH, id_y + BLOCK_WIDTH/2 + 1),
                (id_x + BLOCK_WIDTH, id_y + BLOCK_WIDTH),
                (id_x + BLOCK_WIDTH/2 + 1, id_y + BLOCK_WIDTH)
            ],
            fill="black",
            outline=None
        )

    draw_id_block(START_X - BLOCK_WIDTH - 1, START_Y - BLOCK_WIDTH - 1)
    draw_id_block(
        START_X + len(visrep)*BLOCK_WIDTH + (len(visrep) - 1)*BLOCK_GAP + 1,
        START_Y + len(visrep)*BLOCK_WIDTH + (len(visrep) - 1)*BLOCK_GAP + 1
    )

    '''
    top-right corner is black
    bottom-left corner is white
    '''
    canvas_draw.polygon(
        [
            (START_X + len(visrep)*BLOCK_WIDTH + (len(visrep) - 1)*BLOCK_GAP + 1, START_Y - BLOCK_WIDTH - 1),
            (START_X + len(visrep)*BLOCK_WIDTH + (len(visrep) - 1)*BLOCK_GAP + BLOCK_WIDTH + 1, START_Y - BLOCK_WIDTH - 1),
            (START_X + len(visrep)*BLOCK_WIDTH + (len(visrep) - 1)*BLOCK_GAP + BLOCK_WIDTH + 1, START_Y - BLOCK_WIDTH - 1 + BLOCK_WIDTH),
            (START_X + len(visrep)*BLOCK_WIDTH + (len(visrep) - 1)*BLOCK_GAP + 1, START_Y - BLOCK_WIDTH - 1 + BLOCK_WIDTH)
        ],
        fill="black",
        outline=None
    )

    # Loop through each row of the visrep
    for row in visrep:
        # Loop through each bit of each row
        for bit in row:
            # Draw block, with colour based on bit value
            if bit == 0:
                draw_block("white")
            else:
                draw_block("black")

            # Adjust x coordinate for next block
            live_x += BLOCK_WIDTH + BLOCK_GAP

        # Adjust the location of the x and y coordinates for the next row to be
        # drawn
        live_x = START_X
        live_y += BLOCK_WIDTH + BLOCK_GAP

    # Display the visrep png
    canvas.show()
    canvas.save("test.png","PNG")
