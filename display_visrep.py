from PIL import Image, ImageDraw
from text_to_visrep import *
from constants import *

visrep = generate_visrep("https://www.python.org/dev/peps/pep-0008/#code-lay-out")
live_x, live_y = 150, 150

visrep_display = Image.new('RGB', (1000, 1000), color = (138, 105, 243))
modify_display = ImageDraw.Draw(visrep_display)

for row in visrep:
    for block in row:
        if block == 0:
            top_left = (live_x, live_y)
            top_right = (live_x + BLOCK_WIDTH, live_y)
            bot_left = (live_x, live_y + BLOCK_WIDTH)
            bot_right = (live_x + BLOCK_WIDTH, live_y + BLOCK_WIDTH)
            modify_display.polygon(
                [top_left, top_right, bot_right, bot_left],
                fill="white",
                outline=None
            )
            live_x += BLOCK_WIDTH + BLOCK_GAP
        else:
            top_left = (live_x, live_y)
            top_right = (live_x + BLOCK_WIDTH, live_y)
            bot_left = (live_x, live_y + BLOCK_WIDTH)
            bot_right = (live_x + BLOCK_WIDTH, live_y + BLOCK_WIDTH)
            modify_display.polygon(
                [top_left, top_right, bot_right, bot_left],
                fill="black",
                outline=None
            )
            live_x += BLOCK_WIDTH + BLOCK_GAP
    live_x -= len(row)*(BLOCK_WIDTH + BLOCK_GAP)
    live_y += BLOCK_WIDTH + BLOCK_GAP

visrep_display.show()
