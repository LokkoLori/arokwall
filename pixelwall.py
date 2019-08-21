from neopixel import Adafruit_NeoPixel, Color
import time

class MyPixelWall(Adafruit_NeoPixel):
    def __init__(self, width=20, height=10, orientation=0):
        self.width = width
        self.height = height
        LED_COUNT =  width * height # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 5  # DMA channel to use for generating signal (try 5)
        LED_BRIGHTNESS = 32  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0

        super(MyPixelWall, self).__init__(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

        self.orientation = orientation
        self.begin()

    def calculatePixelIndex(self, x, y):
        if x < 0 or self.width <= x or y < 0 or self.height <= y:
            return -1

        if self.orientation == 0:
            sx = x
            sy = y
            rowlen = self.width
        elif self.orientation == 1:
            sx = self.height - y - 1
            sy = x
            rowlen = self.height
        elif self.orientation == 2:
            sx = self.width - x - 1
            sy = self.height - y - 1
            rowlen = self.width
        elif self.orientation == 3:
            sx = y
            sy = self.width - x
            rowlen = self.height

        #print("%d x %d y %d sx %d sy " % (x, y, sx, sy))
        if sy % 2:
            sx = rowlen - sx - 1 #zig zag
        return sy * rowlen + sx

    def setPixelRGB(self, x, y, r, g, b):
        self.setPixelColor(self.calculatePixelIndex(x,y), Color(g, r, b))

    def getPixelRGB(self, x, y):
        color = self.getPixelColor(self.calculatePixelIndex(x,y))
        b = color % 256
        color = color >> 8
        r = color % 256
        color = color >> 8
        g = color % 256
        return r, g, b

    def blink(self, r, g, b, ms):

        save = []
        for i in range(200):
            save.append(int(self.getPixelColor(i)))
            self.setPixelColor(i, Color(g, r, b))

        self.show()
        time.sleep(ms / 1000.0)

        for i in range(200):
            self.setPixelColor(i, save[i])

        self.show()
