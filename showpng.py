from PIL import Image
from pixelwall import MyPixelWall
import sys


wall = MyPixelWall(orientation=1, width=10, height=20)

if __name__ == '__main__':

    filen = sys.argv[1]
    print(filen)

    img = Image.open(filen)
    rgb_img = img.convert("RGB")
    for y in range(rgb_img.height):
        line = ""
        for x in range(rgb_img.width):
            r, g, b = rgb_img.getpixel((x,y))
            if r:
                line += "o"
            else:
                line += "."
            wall.setPixelRGB(x, y, int(r), int(g), int(b))
        print(line)


    wall.show()