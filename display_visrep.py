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

# Testing
if __name__ == "__main__":
    from text_to_visrep import *
    visrep = generate_visrep("https://www.python.org/dev/peps/pep-0008/#code-lay-out")
    generate_visrep_png(visrep)
