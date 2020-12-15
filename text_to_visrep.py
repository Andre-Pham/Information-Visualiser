# Text to visual representation

def num_to_bin_list(num):
    '''
    Converts a given integer to binary in the form of a list, with each
    element holding a bit. Returns the list.
    '''
    # Converts number to binary
    binary_num = bin(num)
    # Converts binary to list representation and returns it
    bin_list = [int(i) for i in binary_num[2:]]
    return bin_list

def len_to_ten(bin_list):
    '''
    Adds 0s as elements to the front of a list until the list has ten elements.
    Returns the adjusted list.
    '''
    # Add 0s to the front of the list until it has a length of ten
    while len(bin_list) < 10:
        bin_list.insert(0, 0)
    # Return the list
    return bin_list

def generate_visrep(input_text):
    '''
    Generates the visual representation of a string in the form of a 2D matrix
    (nested lists) with 0s and 1s as elements. Returns the visual
    representation.
    '''
    # Define the visual representation to be returned
    visrep = []

    # Loop through every letter of the input text
    for order, letter in enumerate(input_text):
        # Generate binary-list form of the number representation of the
        # character
        num_representation = ord(letter.lower())
        bin_letter_list = len_to_ten(num_to_bin_list(num_representation))
        # Define is_capital as 0 if the letter isn't capital, and 1 if it is
        is_capital = 0
        if letter.isupper():
            is_capital = 1
        # Generate the binary-list form of the location of the character
        bin_location_list = len_to_ten(num_to_bin_list(order))
        # Add the letter's visual representation to the final text's visual
        # representation
        visrep.append(bin_letter_list + [is_capital] + bin_location_list)

    # Return the visual representation
    return visrep

# Testing
if __name__ == "__main__":
    test = generate_visrep("test ")
    for row in test:
        print(row)
