#!/usr/bin/python

import os, sys
from PIL import Image

width = 320
height = 240

# heatmap
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return (r, g, b)

# SIT parser
class SIT:
    def __init__(self, filename):
        f = open(filename, 'r')

        # hardware model this image was taken with
        self.hardware = f.read(7)
        print "Hardware: Mikron M"+self.hardware
        
        # unidentified binary data
        f.read(86)
        
        # timestamp of snapshot
        self.year  = f.read(4)
        self.month = f.read(2)
        self.day   = f.read(2)
        self.hour  = f.read(2)
        self.minute= f.read(2)
        self.second= f.read(2)
        
        # unidentified binary data
        f.read(921)

        # create a new black image
        self.image = Image.new('RGB', (width,height), "black")

        # create the pixel map
        pixels = self.image.load()

        for y in range(height):
            for x in range(width):
                pixels[x,y] = rgb(0, 0x0FFF, (ord(f.read(1))*256 + ord(f.read(1))) & 0x0FFF ) #(ord(f.read(1)), 0, 0)

sit = SIT(sys.argv[1])

sit.image.show()
