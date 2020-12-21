
from PIL import Image

test_list = []
chunk_pixels = 0
img = Image.open("test.png")

img_color = Image.Image.getdata(img).convert("P")
for i in img_color:
    if i != 205:
        test_list.append(i)

def scan_visrep(color_list):
    #get the number of pixels per chunck
    chunk_pixels = color_list.index(225)*2

    #generate squence of each pixel row
    count = 1
    length = []
    for i in range(1,len(color_list)):
        if color_list[i-1] == color_list[i]:
            count += 1
        else:
            #if its 8 the print identity
            if count == chunk_pixels/2:
                length.append("identity")

            #else divid by chunk size and repeat that many time of color
            if count >= chunk_pixels:
                repeats = int(count/chunk_pixels)
                for j in range(repeats):
                    if color_list[i-1] == 225:
                        length.append("White")
                    elif color_list[i-1] == 0:
                        length.append("Black")
                    else:
                        length.append(" Other ")
            #reset count
            count=1

    #find row size
    i = 2
    row_size = 1
    while length[i] != "identity":
        row_size += 1
        i += 1

    #group the same rows together
    output = []
    length.pop(0)
    grouped_list = list(zip(*[iter(length)]*row_size))
    for x in grouped_list:
        if x not in output:
            output.append(x)

    return output


print(scan_visrep(test_list))
print(img.width)
'''
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
black = 0
white = 225

purple = 205
'''
