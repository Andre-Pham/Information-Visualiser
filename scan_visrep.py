
from PIL import Image

img = Image.open("test.png")

img_color = Image.Image.getdata(img).convert("P")
for i in img_color:
    if i != 205:
        print(i)

print(img.width)
'''
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
black = 0
white = 225

purple = 205
'''

#poop
