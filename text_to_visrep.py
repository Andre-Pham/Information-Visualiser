# Code to generate visual representation from text

# Import modules
import math
# Import complimenting scripts
from constants import *

def is_square(num):
    '''
    Determines if a given integer is a perfect square. Returns True if it is,
    otherwise returns False.
    '''
    return num == math.isqrt(num)**2

def num_to_bin_list(num):
    '''
    Converts a given integer to binary in the form of a list, with each
    element holding a bit. Returns the list.
    '''
    # Converts number to binary string
    binary_num = bin(num)
    # Converts binary string to list representation and returns it
    bin_list = [int(i) for i in binary_num[2:]]
    return bin_list

def len_to_dyn(bin_list, dyn):
    '''
    Adds 0s as elements to the front of a list until the list has a given
    (dynamic) number of elements. Returns the adjusted list.
    '''
    # Add 0s to the front of the list until it has a length of dyn
    while len(bin_list) < dyn:
        bin_list.insert(0, 0)
    # Return the list
    return bin_list

def generate_visrep(input_text):
    '''
    Generates the visual representation of a string in the form of a 2D matrix
    (nested lists) with 0s and 1s as elements. Returns the visual
    representation.
    '''
    # Determine how many bits is required to represent each character
    num_reps = [ord(char.lower()) for char in input_text]
    largest_num_rep = max(num_reps)
    char_list_length = len(bin(largest_num_rep)) - 2

    # Define how many blocks the visrep currently has (before adding zeros to
    # the end to make the block count a perfect square)
    num_blocks = (char_list_length + 1)*len(input_text) + INIT_BIT_COUNT

    # Define the number of blocks (0s) to be added to make the total count a
    # perfect square
    new_block_count = 0
    # Determine the number of blocks to be added to the visrep, as well as the
    # final total amount of blocks that will make up the visrep
    while is_square(num_blocks) == False:
        new_block_count += 1
        num_blocks += 1

    # Define the list of 0s to be added to the visrep to make the total block
    # count a perfect square
    new_block_addition = [0 for _ in range(new_block_count)]

    # Define the visual representation to be returned, starting with the number
    # of bits required to represent each character (in binary)
    visrep = len_to_dyn(
        num_to_bin_list(char_list_length + 1),
        INIT_BIT_COUNT
    )

    # Loop through every letter of the input text
    for order, letter in enumerate(input_text):
        # Generate binary-list form of the number representation of the
        # character
        num_representation = ord(letter.lower())
        bin_letter_list = len_to_dyn(
            num_to_bin_list(num_representation),
            char_list_length
        )
        # Define is_capital as 0 if the letter isn't capital, and 1 if it is
        is_capital = 0
        if letter.isupper():
            is_capital = 1
        # Add the letter's visual representation to the final text's visual
        # representation
        visrep += bin_letter_list + [is_capital]

    # Add the final blocks to make len(visrep) a perfect square
    visrep += new_block_addition

    # Create visrep as a 2D matrix with equal rows and columns
    visrep_nested = []
    row_length = math.isqrt(num_blocks)
    for i in range(0, num_blocks, row_length):
        visrep_nested.append(visrep[i:i+row_length])

    # Return the visual representation
    return visrep_nested

# Testing
if __name__ == "__main__":
    test = generate_visrep("https://www.python.org/dev/peps/pep-0008/#code-lay-out")
    for row in test:
        print(row)
