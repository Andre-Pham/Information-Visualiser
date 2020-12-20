# Code to generate text from visual representations

# Import complimenting scripts
from constants import *

def binlist_to_int(bin_list):
    '''
    Generates an integer from a list which contains 0s and 1s to represent a
    binary value.
    '''
    # Convert the list to a string which represents the binary datatype
    bin_string = "0b" + "".join(list(map(str, bin_list)))
    # Converts the binary value to an integer, and returns it
    num = int(bin_string, 2)
    return num

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
    char_bits_len = binlist_to_int(flat_visrep[1:INIT_BIT_COUNT+1])

    # Loop through the index of the beginning of every group of bits which
    # represent a character
    for i in range(INIT_BIT_COUNT+1, len(flat_visrep)-1, char_bits_len):
        # Define the list of bits which represents a character
        char_bits = flat_visrep[i:i+char_bits_len]
        # Decode the character as a string
        char = chr(binlist_to_int(char_bits[:-1]))
        # Capitalise the character if necessary
        if char_bits[-1] == 1:
            char = char.upper()
        # Add the character to the final string
        decoded_text += char

    # Return the final decoded string
    return decoded_text

# Testing
if __name__ == "__main__":
    from text_to_visrep import *
    test = generate_visrep("https://www.python.org/dev/peps/pep-0008/#code-lay-out")
    for row in test:
        print(row)
    print(decode_visrep(test))
