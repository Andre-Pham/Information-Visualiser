# Code to generate visual representation from text

# Import modules
import math
# Import complimenting scripts
from constants_dev import *

def is_square(num):
    '''
    Determines if a given integer is a perfect square. Returns True if it is,
    otherwise returns False.

    PARAMETERS:
        num = an integer
    OUTPUT:
        If num is a perfect square number, True. If not, False.
    '''
    return num == math.isqrt(num)**2

def num_to_bin_list(num):
    '''
    Converts a given integer to binary in the form of a list, with each
    element holding a bit. Returns the list.

    PARAMETERS:
        num = an integer
    OUTPUT:
        bin_list = the integer input in binary, represented as a list, e.g.
            if num=3, bin_list=[1, 0, 1]
    '''
    # Converts number to binary string
    bin_string = bin(num)
    # Converts binary string to list representation and returns it
    bin_list = [int(i) for i in bin_string[2:]]
    return bin_list

def len_to_dyn(bin_list, num):
    '''
    Adds 0s as elements to the front of a list until the list has a given
    number (num) of elements. Returns the adjusted list.

    PARAMETERS:
        bin_list = a binary value represented as a list
        num = an integer that you would like the the length of bin_list to be
    OUTPUT:
        bin_list = bin_list input, but with 0 elements added to the front so
            that its length is num
    '''
    # Add 0s to the front of the list until it has a length of num
    while len(bin_list) < num:
        bin_list.insert(0, 0)
    # Return the list
    return bin_list

def gen_visrep_matrix(text):
    '''
    Generates the visual representation of a string in the form of a 2D matrix
    (nested lists) with 0s and 1s as elements. Returns the visual
    representation.

    PARAMETERS:
        text = a string to be converted
    OUTPUT:
        visrep_matrix = a 2D matrix (nested lists) that represents the text
    '''
    # Determine how many bits is required to represent each character
    all_ascii_used = [ord(char.lower()) for char in text]
    if len(all_ascii_used) == 0:
        char_bits_len = 0
    else:
        max_ascii = max(all_ascii_used)
        char_bits_len = len(bin(max_ascii)) - 2

    # Define how many blocks the visrep currently has (before adding zeros to
    # the end to make the block count a perfect square)
    num_blocks = (char_bits_len + 1)*len(text) + INIT_BIT_COUNT + 4

    # Define the number of blocks (0s) to be added to make the total count a
    # perfect square
    num_extra_blocks = 0
    # Determine the number of blocks to be added to the visrep, as well as the
    # final total amount of blocks that will make up the visrep
    while is_square(num_blocks) == False:
        num_extra_blocks += 1
        num_blocks += 1

    # Define the list of 0s to be added to the visrep to make the total block
    # count a perfect square
    extra_blocks = [0 for _ in range(num_extra_blocks)]

    # Define the visual representation to be returned, starting with the
    # identity block, then the the number of bits required to represent each
    # character (in binary)
    visrep_flat = len_to_dyn(
        num_to_bin_list(char_bits_len + 1),
        INIT_BIT_COUNT
    )
    # Define row length
    row_len = math.isqrt(num_blocks)

    # Loop through every character of the input text
    for char in text:
        # Generate binary-list form of the number representation of the
        # character
        num_representation = ord(char.lower())
        bin_char_list = len_to_dyn(
            num_to_bin_list(num_representation),
            char_bits_len
        )
        # Define is_capital as 0 if the char isn't capital, and 1 if it is
        is_capital = 0
        if char.isupper():
            is_capital = 1
        # Add the character's visual representation to the final text's visual
        # representation
        visrep_flat += bin_char_list + [is_capital]

    # Add first two identity blocks
    visrep_flat.insert(0, "I1")
    visrep_flat.insert(row_len-1, "I2")
    # Add the extra blocks to make len(visrep_flat) a perfect square
    visrep_flat += extra_blocks
    # Add last two identity blocks
    visrep_flat.insert(num_blocks-row_len, "I3")
    visrep_flat.append("I4")

    # Create visrep as a 2D matrix with equal rows and columns
    visrep_matrix = []
    for i in range(0, num_blocks, row_len):
        visrep_matrix.append(visrep_flat[i:i+row_len])

    # Return the visual representation
    return visrep_matrix
