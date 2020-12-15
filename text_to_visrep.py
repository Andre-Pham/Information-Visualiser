# Text to visual representation

#input_text = input("What would you like to convert to a visual representation?\n")

def num_to_bin_list(num):
    binary_num = bin(num)
    bin_list = [int(i) for i in binary_num[2:]]
    return bin_list

def len_to_ten(bin_list):
    while len(bin_list) < 10:
        bin_list.insert(0, 0)
    return bin_list

def generate_visrep(input_text):
    visrep = []
    for order, letter in enumerate(input_text):
        num_representation = ord(letter.lower())
        bin_letter_list = len_to_ten(num_to_bin_list(num_representation))
        is_capital = 0
        if letter.isupper():
            is_capital = 1
        bin_location_list = len_to_ten(num_to_bin_list(order))
        visrep.append(bin_letter_list + [is_capital] + bin_location_list)
    return visrep

if __name__ == "__main__":
    test = generate_visrep("test ")
    for row in test:
        print(row)
