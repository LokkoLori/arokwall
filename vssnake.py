import colorsys

from pixelwall import MyPixelWall
import time
from gamepadcode import GamePadBase
import colorsys

class SnakeController(GamePadBase):

    def up_down(self):
        super(SnakeController, self).up_down()
        if self.snake.y_velo == 1:
            return
        self.snake.y_velo = -1
        self.snake.x_velo = 0


    def down_down(self):
        super(SnakeController, self).down_down()
        if self.snake.y_velo == -1:
            return
        self.snake.y_velo = 1
        self.snake.x_velo = 0

    def left_down(self):
        super(SnakeController, self).down_down()
        if self.snake.x_velo == 1:
            return
        self.snake.y_velo = 0
        self.snake.x_velo = -1


    def right_down(self):
        super(SnakeController, self).down_down()
        if self.snake.x_velo == -1:
            return
        self.snake.y_velo = 0
        self.snake.x_velo = 1

    def __init__(self, snake):
        super(SnakeController, self).__init__(input=("/dev/input/js%d" % snake.id))
        self.snake = snake


class Snake(object):

    def __init__(self, id=0):
        self.x_pos = 0
        self.y_pos = 0
        self.r = 255
        self.g = 255
        self.b = 255
        self.x_velo = 0
        self.y_velo = 0
        self.id = id
        self.hp = 100
        self.oc = 0

        self.idlec = 0

        self.controller = SnakeController(self)

    def step(self):
        self.x_pos += self.x_velo
        self.y_pos += self.y_velo
        if 19 < self.x_pos:
            self.x_pos = 19
            self.x_velo = 0
            return 1
        elif self.x_pos < 0:
            self.x_pos = 0
            self.x_velo = 0
            return 1
        if 9 < self.y_pos:
            self.y_pos = 9
            self.y_velo = 0
            return 1
        elif self.y_pos < 0:
            self.y_pos = 0
            self.y_velo = 0
            return 1

        return 0




fade = 0.8
bw = 10
hm = 0.1
th = 10
moc = 10
snakes = []
snakes.append(Snake(id=len(snakes)))
snakes.append(Snake(id=len(snakes)))

def snakesinit():

    snakes[0].r = 255
    snakes[0].g = 255
    snakes[0].b = 0

    snakes[0].x_pos = 4
    snakes[0].y_pos = 3
    snakes[0].x_velo = 0
    snakes[0].y_velo = 0
    snakes[0].hp = 100

    snakes[1].r = 0
    snakes[1].g = 255
    snakes[1].b = 255

    snakes[1].x_pos = 15
    snakes[1].y_pos = 6
    snakes[1].x_velo = 0
    snakes[1].y_velo = 0
    snakes[1].hp = 100

def normcolor(r, g, b):
    if r:
        r = 1
    if g:
        g = 1
    if b:
        b = 1

    return [r, g, b]

def colorvolume(r, g, b):
    if r:
        return r / 256.0
    if g:
        return g / 256.0
    if b:
        return b / 256.0

def snakebite(r, g, b):

    for s in snakes:
        if normcolor(s.r, s.g, s.b) == normcolor(r, g, b):
            hurt = int(colorvolume(r, g, b)*50)
            print("%d hurt : %d" % (s.id, hurt))
            s.hp -= hurt


if __name__ == '__main__':

    wall = MyPixelWall(orientation=2)

    snakesinit()

    h = 0
    while True:

        # rgb = colorsys.hsv_to_rgb(h / 256.0, 1.0, 1.0)
        # h += 16
        #
        # if 255 < h:
        #     h = 0
        #
        # snakes[0].r = int(rgb[0] * 255)
        # snakes[0].g = int(rgb[1] * 255)
        # snakes[0].b = int(rgb[2] * 255)

        time.sleep(5 / 1000.0)

        idle = True
        for s in snakes:

            s.idlec += 1
            if bw+(100-s.hp)*hm < s.idlec:
                s.idlec = 0
                # wall.setPixelRGB(s.x_pos, s.y_pos, s.r, s.g, s.b)
                crash = s.step()

                r, g, b = wall.getPixelRGB(s.x_pos, s.y_pos)
                if (s.x_velo or s.y_velo) and (th < r or th < g or th < b):
                    if s.oc == 0:
                        #one snake was bitten
                        wall.blink(r, g, b, 20)
                        snakebite(r, g, b)
                    s.oc += 1
                    if moc < s.oc:
                        s.oc = 10
                else:
                    s.oc = 0

                # wall.setPixelRGB(s.x_pos, s.y_pos, 255, 255, 255)
                wall.setPixelRGB(s.x_pos, s.y_pos, s.r, s.g, s.b)
                idle = False
                if crash:
                    s.hp -= 5
                    wall.blink(s.r, s.g, s.b, 20)

            if s.hp < 0:
                for n in range(5):
                    wall.blink(s.r, s.g, s.b, 200)
                    time.sleep(200 / 1000.0)
                snakesinit()

        if idle:
            continue

        for y in range(10):
            for x in range(20):
                r, g, b = wall.getPixelRGB(x,y)
                wall.setPixelRGB(x, y, int(r*fade), int(g*fade), int(b*fade))

        wall.show()



