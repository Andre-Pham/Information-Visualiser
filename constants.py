# Defines the constants that the other files use, for quick access

# Determine if the OS is MacOS (used for determining directories, logo and font)
import sys
if sys.platform.startswith("darwin"):
    MAC = True
    MAC_DIR = __file__[:__file__.rfind("/")+1]
else:
    MAC = False

# Define how many pixels wide are the blocks that make up the visrep
BLOCK_WIDTH = 40

# Define how many pixels between each block that makes up the visrep
BLOCK_GAP = BLOCK_WIDTH/4

# Define how many bits are at the start of the visrep to represent how many bits
# in a row represent a character
INIT_BIT_COUNT = 4

# Define RGB background colour for displaying visrep png
VISREP_BG_PURPLE = (126, 86, 251)
VISREP_BG_RED = (233, 43, 43)
VISREP_BG_GREEN = (88, 172, 57)
VISREP_BG_BLUE = (48, 128, 233)
VISREP_BG_PINK = (233, 50, 170)

# Define top-left starting pixel coordinate for visrep png
START_X, START_Y = 80, 80

# Define minimum BGR value difference for the sum of R, G and B to be treated as
# a different colour (smaller = more sensitive to differences)
BGR_THRESHOLD = 95

# Define minimum BGR value difference for one of R, G or B to be treated as a
# different colour (smaller = more sensitive to differences)
BGR_CHANNEL_THRESHOLD = 90

# Define brightness threshold, based on sum([255, 255, 255])/2
BRIGHTNESS_THRESHOLD = 382.5

# Define max length for an image before it's resized
MAX_LENGTH = 1200

# Define how many pixels the reference identity blocks are expanded by for each
# iteration of searching for a match
ID_RESIZE_INCREMENT = 8
ID_RESIZE_COMPOUND = 1.5

# Define how long the reference identity blocks must be before compounding size
ID_RESIZE_COMPOUND_THRESHOLD = 42

# Define aesthetic interface constants
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"
TEXT_COLOR_HIGHLIGHT = "white"
if MAC:
    TEXT_COLOR_HIGHLIGHT = "black"
TEXTBOX_COLOR = "#d0d0d0"
BUTTON_COLOR = "#7e56fb"
FONT = "System"
SUCCESS_COLOR = "#22c95d"
FAIL_COLOR = "#ee4f4f"
LOAD_COLOR = "#ffad14"
BUTTON_WIDTH = 14

# Define directory of identity block reference images
DIR_ID1 = "resources/identity1.png"
DIR_ID2 = "resources/identity2.png"
DIR_ID3 = "resources/identity3.png"
DIR_ID4 = "resources/identity4.png"
if MAC:
    DIR_ID1 = MAC_DIR + DIR_ID1
    DIR_ID2 = MAC_DIR + DIR_ID2
    DIR_ID3 = MAC_DIR + DIR_ID3
    DIR_ID4 = MAC_DIR + DIR_ID4

# Define directory of logo
DIR_LOGO = "resources/logo.ico"
