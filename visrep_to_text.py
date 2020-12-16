# Visual representation to text

# Import complimenting scripts
from text_to_visrep import *
from constants import *

def binlist_to_int(binlist):
    '''
    Generates an integer from a list which contains 0s and 1s to represent a
    binary value.
    '''
    # Convert the list to a string which represents the binary datatype
    bin_representation = "0b" + "".join(list(map(str, binlist)))
    # Converts the binary value to an integer, and returns it
    num_representation = int(bin_representation, 2)
    return num_representation

def decode_visrep(visrep):
    '''
    Generates the string from its visual representation, which is a 2D matrix
    (nested lists) which holds 0s and 1s. Returns the string.
    '''
    # Define the string to be returned as a list
    decoded_text = ""
    # Define the visrep 2D matrix as a flattened list
    flat_visrep = [bit for row in visrep for bit in row]
    # Define how many bits in a row represents a character
    char_list_len = binlist_to_int(flat_visrep[:INIT_BIT_COUNT])

    # Loop through the index of the beginning of every group of bits which
    # represent a character
    for i in range(INIT_BIT_COUNT, len(flat_visrep), char_list_len):
        # Define the list of bits which represents a character
        letter_rep = flat_visrep[i:i+char_list_len]
        # Decode the character as a string
        letter = chr(binlist_to_int(letter_rep[:-1]))
        # Capitalise the letter if necessary
        if letter_rep[-1] == 1:
            letter = letter.upper()
        # Add the character to the final string
        decoded_text += letter

    # Return the final decoded string
    return decoded_text

# Testing
if __name__ == "__main__":
    test = generate_visrep("https://www.python.org/dev/peps/pep-0008/#code-lay-out")
    for row in test:
        print(row)
    print(decode_visrep(test))
