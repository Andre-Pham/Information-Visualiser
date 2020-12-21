import cv2
from PIL import Image, ImageDraw

test_list = []
chunk_pixels = 0
img = Image.open("test.png")

img_color = Image.Image.getdata(img).convert("P")



def find_identity_start():

    method = cv2.TM_SQDIFF_NORMED

    # Read the images from the file
    small_image = cv2.imread('identity_start.png')
    large_image = cv2.imread('test.png')

    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

    # Display the original image with the rectangle around the match.
    cv2.imshow('output',large_image)

    # The image is only displayed if we call this
    cv2.waitKey(0)

def find_identity_end():
    method = cv2.TM_SQDIFF_NORMED

    # Read the images from the file
    small_image = cv2.imread('identity_end.png')
    large_image = cv2.imread('test.png')

    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

    # Display the original image with the rectangle around the match.
    cv2.imshow('output',large_image)

    # The image is only displayed if we call this
    cv2.waitKey(0)

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

find_identity_start()

'''
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
black = 0
white = 225

purple = 205
'''
