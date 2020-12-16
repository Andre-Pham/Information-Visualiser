# Defines the constants that the other files use, for quick access

# Define how many pixels wide are the blocks that make up the visrep
BLOCK_WIDTH = 15

# Define how many pixels between each block that makes up the visrep
BLOCK_GAP = BLOCK_WIDTH/3

# Define how many bits are at the start of the visrep to represent how many bits
# in a row represent a character
INIT_BIT_COUNT = 4

# Define RGB background colour for displaying visrep png
BACKGROUND_COLOR = (138, 105, 243)

# Define top-left starting pixel coordinate for visrep png
START_X, START_Y = 150, 150

# Define png size, in pixels
PNG_SIZE = (1000, 1000)
