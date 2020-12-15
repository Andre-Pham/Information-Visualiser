# Visual representation to text

# Import complimenting scripts
from text_to_visrep import *

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
        letter_bin_representation = "0b" + "".join(list(map(str, letter_rep[0:10])))
        letter_num_representation = int(letter_bin_representation, 2)
        letter = chr(letter_num_representation)
        # Capitalise the letter if necessary
        if letter_rep[10] == 1:
            letter = letter.upper()
        # Decode the location of the character
        location_bin_representaiton = "0b" + "".join(list(map(str, letter_rep[12:22])))
        location_num_representation = int(location_bin_representaiton, 2)
        # Insert the character into its correct location in decoded_text_as_list
        decoded_text_as_list.insert(location_num_representation, letter)

    # Return decoded_text_as_list as a string, which is the final decoded string
    return "".join(decoded_text_as_list)

# Testing
if __name__ == "__main__":
    test = generate_visrep("This is a test statement.")
    for row in test:
        print(row)
    print(decode_visrep(test))
