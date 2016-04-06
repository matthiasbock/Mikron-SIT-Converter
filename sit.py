#!/usr/bin/python

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

        self.data = []
        self.min = 0x3FFF
        self.max = 0
        for y in range(height):
            row = []
            for x in range(width):
                value = (ord(f.read(1))*256 + ord(f.read(1))) & 0x0FFF
                row.append(value)
                if value > self.max:
                    self.max = value
                if value < self.min:
                    self.min = value
            self.data.append(row)

        self.image = None

    def create_image(self):
        # create a new black image
        self.image = Image.new('RGB', (width,height), "black")

        # create the pixel map
        pixels = self.image.load()
        
        for y in range(height):
            for x in range(width):
                pixels[x,y] = rgb(self.min, self.max, self.data[y][x])

    def show(self):
        if self.image is None:
            create_image()
        self.image.show()

    def saveas(self, filename, format):
        if self.image is None:
            create_image()
        self.image.save(filename, format)
