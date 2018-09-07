# -*- coding: utf-8 -*-
from PIL import Image

import os

img = Image.open("facemask1.png")
img = img.convert("RGBA")
pixdata = img.load()

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x,y][0]>220 and pixdata[x,y][1]>220 and pixdata[x,y][2]>220 and pixdata[x,y][3]>220:
            pixdata[x, y] = (255, 255, 255, 0)
img.save("facemask.png", "PNG")