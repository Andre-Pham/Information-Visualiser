# Visual representation to text

from text_to_visrep import *

def decode_visrep(visrep):
    decoded_text_as_list = []
    for letter_rep in visrep:
        letter_bin_representation = "0b" + "".join(list(map(str, letter_rep[0:10])))
        letter_num_representation = int(letter_bin_representation, 2)
        letter = chr(letter_num_representation)

        if letter_rep[10] == 1:
            letter = letter.upper()

        location_bin_representaiton = "0b" + "".join(list(map(str, letter_rep[12:22])))
        location_num_representation = int(location_bin_representaiton, 2)

        decoded_text_as_list.insert(location_num_representation, letter)
    return "".join(decoded_text_as_list)

if __name__ == "__main__":
    test = generate_visrep("that's my girl wh]][[]]")
    for row in test:
        print(row)
    print(decode_visrep(test))
