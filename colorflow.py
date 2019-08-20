# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import colorsys

from pixelwall import MyPixelWall
from gamepadcode import GamePadBase

d = -1

class MyGamePad(GamePadBase):

    def up_down(self):
        super(MyGamePad, self).up_down()
        global d
        #print("fel")
        d = 1

    def down_down(self):
        super(MyGamePad, self).down_down()
        global d
        #print("le")
        d = -1

    def __init__(self):
        super(MyGamePad, self).__init__()


# Main program logic follows:
if __name__ == '__main__':

    wall = MyPixelWall()
    mgp = MyGamePad()

    print('Press Ctrl-C to quit.')
    h = 0
    s = 255
    while True:
        h = s
        for y in range(10):
            for x in range(20):
                rgb = colorsys.hsv_to_rgb(h/256.0, 1.0, 1.0)
                wall.setPixelRGB(x,y, int(rgb[0]*255.0), int(rgb[1]*255.0), int(rgb[2]*255.0))
                h += 2
                if h > 255:
                    h = 0
        wall.show()
        s += d
        if s < 0:
            s = 255
        if 255 < s:
            s = 0
