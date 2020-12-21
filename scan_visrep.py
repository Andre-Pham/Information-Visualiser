import cv2

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

    print(large_image[156][156])

    return (MPx+1, MPy+1)

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

    return (MPx+1, MPy+1)

def scan_visrep(start_x, start_y, end_x, end_y):
    image = cv2.imread('test.png')

    count = 0
    x = start_x + 1
    #find chunck size
    while image[x][start_y] == [255, 255, 255]:
        count += 1
        x += 1
    print(count)



start_x, start_y = find_identity_start()
end_x, end_y = find_identity_end()
print(scan_visrep(start_x, start_y, end_x, end_y))

'''
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
black = 0
white = 225

purple = 205
'''
