
from PIL import Image, ImageDraw

test_list = []
chunk_pixels = 0
img = Image.open("test.png")

img_color = Image.Image.getdata(img).convert("P")



def find_identity():
    im = Image.open ('test.png')
    isize = im.size
    identity = Image.open ('identity.png')
    identity_size = identity.size
    x0, y0 = identity_size [0] // 2, identity_size [1] // 2
    pixel = identity.getpixel ( (x0, y0) ) [:-1]

    def diff (a, b):
        return sum ( (a - b) ** 2 for a, b in zip (a, b) )

    best = (10000, 0, 0)
    for x in range (isize [0] ):
        for y in range (isize [1] ):
            ipixel = im.getpixel ( (x, y) )
            d = diff (ipixel, pixel)
            if d < best [0]: best = (d, x, y)

    draw = ImageDraw.Draw (im)
    x, y = best [1:]
    draw.rectangle ( (x - x0, y - y0, x + x0, y + y0), outline = 'red')
    im.save ('out.png')

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

    #remove anything before identity
    length.pop(0)


    #group the same rows together
    output = []
    grouped_list = list(zip(*[iter(length)]*row_size))
    for x in grouped_list:
        if x not in output:
            output.append(x)
    print(length)
    return output

find_identity()

'''
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
black = 0
white = 225

purple = 205
'''
