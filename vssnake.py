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
        self.stepped = False

        self.controller = SnakeController(self)

    def step(self):

        crush = False
        self.stepped = False
        pre_x = int(self.x_pos)
        pre_y = int(self.y_pos)
        multi = ((self.hp + 50) * 0.004)
        self.x_pos += self.x_velo * multi
        self.y_pos += self.y_velo * multi


        if wall.width - 1 < self.x_pos:
            self.x_pos = wall.width - 1
            self.x_velo = 0
            crush = True
        elif self.x_pos < 0:
            self.x_pos = 0
            self.x_velo = 0
            crush = True
        if wall.height - 1 < self.y_pos:
            self.y_pos = wall.height - 1
            self.y_velo = 0
            crush = True
        elif self.y_pos < 0:
            self.y_pos = 0
            self.y_velo = 0
            crush = True

        if int(self.x_pos) != pre_x or int(self.y_pos) != pre_y:
            self.stepped = True

        return crush

    def isActive(self):
        return s.controller.status["connected"]


wall = MyPixelWall(orientation=1, width=10, height=20)

playfield = []
for y in range(wall.height):
    row = []
    for x in range(wall.width):
        row.append([0, 0, 0, 0])
    playfield.append(row)

stampmap = []
for y in range(wall.height):
    row = []
    for x in range(wall.width):
        row.append([0, 0, 0])
    stampmap.append(row)


death = """
.ooo.
ooooo
o o o
ooooo
.o.o.
"""

bite = """
o...o
.ooo.
oo oo
.ooo.
o...o
"""

fade = 0.8
stampfade = 0.9
bw = 10
hm = 0.1
th = 10
moc = 10
snakes = []
snakes.append(Snake(id=len(snakes)))
snakes.append(Snake(id=len(snakes)))
snakes.append(Snake(id=len(snakes)))
snakes.append(Snake(id=len(snakes)))

def snakesinit():

    snakes[0].r = 255
    snakes[0].g = 255
    snakes[0].b = 0

    snakes[0].x_pos = 3
    snakes[0].y_pos = 2
    snakes[0].x_velo = 0
    snakes[0].y_velo = 0
    snakes[0].hp = 100

    snakes[1].r = 0
    snakes[1].g = 255
    snakes[1].b = 255

    snakes[1].x_pos = wall.width - 4
    snakes[1].y_pos = wall.height - 3
    snakes[1].x_velo = 0
    snakes[1].y_velo = 0
    snakes[1].hp = 100

    snakes[2].r = 255
    snakes[2].g = 0
    snakes[2].b = 255

    snakes[2].x_pos = 3
    snakes[2].y_pos = wall.height - 3
    snakes[2].x_velo = 0
    snakes[2].y_velo = 0
    snakes[2].hp = 100

    snakes[3].r = 255
    snakes[3].g = 255
    snakes[3].b = 255

    snakes[3].x_pos = wall.width - 4
    snakes[3].y_pos = 2
    snakes[3].x_velo = 0
    snakes[3].y_velo = 0
    snakes[3].hp = 100

    for y in range(wall.height):
        for x in range(wall.width):
            playfield[y][x] = [0.0,0.0,0.0,0.0]

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


def rollo(r, g, b):
    for y in range(wall.height):
        for x in range(wall.width):
            wall.setPixelRGB(x, y, r, g, b)
            time.sleep(0.002)
            wall.show()


def stamp(stmp, cx, cy, r, g, b):
    lns = stmp.split('\n')
    lns = lns[1:-1]
    print(lns)
    for y in range(5):
        for x in range(5):
            if lns[y][x] == "o":
                sy = cy-2+y
                sx = cx-2+x
                if 0 <= sx and sx < wall.width and 0 <= sy and sy < wall.height:
                    stampmap[sy][sx] = [r, g, b]

if __name__ == '__main__':

    snakesinit()

    h = 0

    rh = 0
    rs = 255
    rd = 1
    happyrun = 0
    winner = None

    rollo(255, 0, 0)

    while True:

        time.sleep(10 / 1000.0) #let the other thread breath !
        actsnakes_count = 0

        #everybody moves
        for s in snakes:

            if not s.isActive() or not s.hp:
                continue

            actsnakes_count += 1

            # wall.setPixelRGB(s.x_pos, s.y_pos, s.r, s.g, s.b)
            crash = s.step()
            sx = int(s.x_pos)
            sy = int(s.y_pos)

            playfield[sy][sx][s.id] = 1.0



        if actsnakes_count == 0:
            
            #rainbow idle ...
            rh = rs
            for y in range(wall.height):
                for x in range(wall.width):
                    rgb = colorsys.hsv_to_rgb(rh / 256.0, 1.0, 1.0)
                    wall.setPixelRGB(x, y, int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0))
                    rh += 2
                    if rh > 255:
                        rh = 0
            wall.show()
            rs += rd
            if rs < 0:
                rs = 255
            if 255 < rs:
                rs = 0

            continue

        if happyrun:

            happyrun -= 1
            if happyrun == 0:
                snakesinit()
                rollo(winner.r, winner.g, winner.b)

        if 1 < actsnakes_count:
            #snakebites
            for s in [s for s in snakes if s.stepped]:
                sx = int(s.x_pos)
                sy = int(s.y_pos)
                for e in [e for e in snakes if e.hp and e.id != s.id]:
                    em = playfield[sy][sx][e.id]
                    if 0.1 < em:
                        #enemy snake was bitten
                        e.hp -= 33 * em
                        print("snake %d has bitten snake %d ... ramining hp = %d" % (s.id, e.id, e.hp))
                        if e.hp <= 0:
                            #enemy snake died
                            print("snake %d died" % e.id)
                            e.hp = 0
                            stamp(death, int(e.x_pos), int(e.y_pos), e.r, e.g, e.b)
                            s.hp += 33
                        else:
                            em *= 0.5
                            stamp(bite, int(s.x_pos), int(s.y_pos), int(em * e.r), int(em * e.g), int(em * e.b))

            #last snake standing
            standings = [s for s in snakes if s.hp and s.isActive()]
            if len(standings) == 1:
                #we've got a winner!
                s = standings[0]
                print("snake %d WINS" % s.id)
                happyrun = 50
                winner = s
                continue

            if len(standings) == 0:
                #tie
                snakesinit()
                rollo(255, 0, 0)
                continue


        #draw and fade playfiled
        for y in range(wall.height):
            for x in range(wall.width):

                r = 0
                g = 0
                b = 0
                for s in snakes:
                    playfield[y][x][s.id] *= fade
                    c = playfield[y][x][s.id]
                    r += c * s.r
                    g += c * s.g
                    b += c * s.b

                sr, sg, sb = [c * stampfade for c in stampmap[y][x]]

                r += sr
                g += sg
                b += sb

                stampmap[y][x] = [sr, sg, sb]

                if 255 < r:
                    r = 255
                if 255 < g:
                    g = 255
                if 255 < b:
                    b = 255
                    
                wall.setPixelRGB(x, y, int(r), int(g), int(b))

        wall.show()



