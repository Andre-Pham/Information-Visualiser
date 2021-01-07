# Code for running unit tests

# Import modules
import os
# Import complimenting scripts
from read_visrep_matrix import *
from read_visrep_photo import *

print("-----UNIT TESTS START-----")

dir = os.path.dirname(os.path.realpath(__file__)) + "/EXAMPLES TO TRY/test"

test_num = 1
test_dir = dir + str(test_num)
fails = []
while True:
    if os.path.isfile(dir + str(test_num) + ".jpg"):
        try:
            test_dir = dir + str(test_num) + ".jpg"
            visrep_matrix = read_visrep_photo(test_dir)
            text_output = read_visrep_matrix(visrep_matrix)
            print(f"test{test_num}: {text_output}")
        except:
            print(f"test{test_num}: FAIL")
            fails.append(test_num)
    elif os.path.isfile(dir + str(test_num) + ".png"):
        try:
            test_dir = dir + str(test_num) + ".png"
            visrep_matrix = read_visrep_photo(test_dir)
            text_output = read_visrep_matrix(visrep_matrix)
            print(f"test{test_num}: {text_output}")
        except:
            print(f"test{test_num}: FAIL")
            fails.append(test_num)
    else:
        break
    test_num += 1

print("-----UNIT TESTS COMPLETE-----")
print(f"Failed numbers: {fails}")
