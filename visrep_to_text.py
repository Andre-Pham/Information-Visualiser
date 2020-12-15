# Visual representation to text

# Import complimenting scripts
from text_to_visrep import *

def binlist_to_int(binlist):
    '''
    Generates an integer from a list, which contains 0s and 1s to represent a
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
    (nested lists) which olds 0s and 1s. Returns the string.
    '''
    # Defines the string to be returned as a list
    decoded_text_as_list = []

    # Loops through every nested list in the visrep, which each represents
    # a character
    for letter_rep in visrep:
        # Decode the character as a string
        letter = chr(binlist_to_int(letter_rep[0:10]))
        # Capitalise the letter if necessary
        if letter_rep[10] == 1:
            letter = letter.upper()
        # Decode the location of the character
        location_num_representation = binlist_to_int(letter_rep[12:22])
        # Insert the character into its correct location in decoded_text_as_list
        decoded_text_as_list.insert(location_num_representation, letter)

    # Return decoded_text_as_list as a string, which is the final decoded string
    return "".join(decoded_text_as_list)

def test(test):
    return test + " hello there"

# Testing
if __name__ == "__main__":
    test = generate_visrep("https://www.qr-code-generator.com/")
    for row in test:
        print(row)
    print(decode_visrep(test))
