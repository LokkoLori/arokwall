from neopixel import Adafruit_NeoPixel, Color
import time

class MyPixelWall(Adafruit_NeoPixel):
    def __init__(self, orientation=0):
        LED_COUNT = 200  # Number of LED pixels.
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
        if self.orientation:
            if self.orientation == 1:
                sy = x
                sx = 9 - y
            if self.orientation == 2:
                sx = 19 - x
                sy = 9 - y
            if self.orientation == 3:
                sy = 19 - x
                sx = y

            x = sx
            y = sy

        if y % 2:
            x = 19 - x #zig zag
        return y * 20 + x

    def setPixelRGB(self, x, y, r, g, b):
        self.setPixelColor(self.calculatePixelIndex(x,y), Color(r, g, b))

    def getPixelRGB(self, x, y):
        color = self.getPixelColor(self.calculatePixelIndex(x,y))
        b = color % 256
        color = color >> 8
        g = color % 256
        color = color >> 8
        r = color % 256
        return r, g, b

    def blink(self, r, g, b, ms):

        save = []
        for i in range(200):
            save.append(int(self.getPixelColor(i)))
            self.setPixelColor(i, Color(r, g, b))

        self.show()
        time.sleep(ms / 1000.0)

        for i in range(200):
            self.setPixelColor(i, save[i])

        self.show()
