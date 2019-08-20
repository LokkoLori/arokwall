
import threading
import struct
import time

class GamePadBase(object):

    def dprint(self, s):
        if self.printing:
            print(s)

    def v_up(self):
        self.dprint("v up")
        self.status["v_dir"] = 0

    def h_up(self):
        self.dprint("h up")
        self.status["h_dir"] = 0

    def X_up(self):
        self.dprint("x up")
        self.status["X"] = 0

    def Y_up(self):
        self.dprint("y up")
        self.status["Y"] = 0

    def A_up(self):
        self.dprint("a up")
        self.status["A"] = 0

    def B_up(self):
        self.dprint("b up")
        self.status["B"] = 0

    def SELECT_up(self):
        self.dprint("select up")
        self.status["SELECT"] = 0

    def START_up(self):
        self.dprint("start up")
        self.status["START"] = 0

    def L_up(self):
        self.dprint("L up")
        self.status["L"] = 0

    def R_up(self):
        self.dprint("R up")
        self.status["R"] = 0

    def left_down(self):
        self.dprint("left down")
        self.status["h_dir"] = -1

    def right_down(self):
        self.dprint("right down")
        self.status["h_dir"] = 1

    def up_down(self):
        self.dprint("up down")
        self.status["v_dir"] = -1

    def down_down(self):
        self.dprint("down down")
        self.status["v_dir"] = 1

    def X_down(self):
        self.dprint("x down")
        self.status["X"] = 1

    def Y_down(self):
        self.dprint("y down")
        self.status["Y"] = 1

    def A_down(self):
        self.dprint("a down")
        self.status["A"] = 1

    def B_down(self):
        self.dprint("b down")
        self.status["B"] = 1

    def SELECT_down(self):
        self.dprint("select down")
        self.status["SELECT"] = 1

    def START_down(self):
        self.dprint("start down")
        self.status["START"] = 1

    def L_down(self):
        self.dprint("L down")
        self.status["L"] = 1

    def R_down(self):
        self.dprint("R down")
        self.status["R"] = 1

    def contoller_loop(self):
        while True:
            try:
                infile_path = self.input
                EVENT_SIZE = struct.calcsize("LhBB")
                file = open(infile_path, "rb")
                event = file.read(EVENT_SIZE)
                while event:
                    #print(struct.unpack("LhBB", event))
                    (tv_msec,  value, type, number) = struct.unpack("LhBB", event)

                    if type == 2:
                        #direction
                        if number == 0:
                            #left-right:
                            if value == 0:
                                self.h_up()
                            elif value < 0:
                                self.left_down()
                            else:
                                self.right_down()
                        elif number == 1:
                            #up-down:
                            if value == 0:
                                self.v_up()
                            elif value < 0:
                                self.up_down()
                            else:
                                self.down_down()
                    elif type == 1:
                        #buttons
                        if number == 0:
                            if value:
                                self.A_down()
                            else:
                                self.A_up()
                        elif number == 1:
                            if value:
                                self.B_down()
                            else:
                                self.B_up()
                        elif number == 2:
                            if value:
                                self.X_down()
                            else:
                                self.X_up()
                        elif number == 3:
                            if value:
                                self.Y_down()
                            else:
                                self.Y_up()
                        elif number == 4:
                            if value:
                                self.L_down()
                            else:
                                self.L_up()
                        elif number == 5:
                            if value:
                                self.R_down()
                            else:
                                self.R_up()
                        elif number == 6:
                            if value:
                                self.SELECT_down()
                            else:
                                self.SELECT_up()
                        elif number == 7:
                            if value:
                                self.START_down()
                            else:
                                self.START_up()


                    event = file.read(EVENT_SIZE)
            except Exception as e:
                file.close()


    def __init__(self, input="/dev/input/js0"):

        self.printing = False
        self.status = {
            "v_dir": 0,
            "h_dir": 0,
            "A": 0,
            "B": 0,
            "X": 0,
            "Y": 0,
            "L": 0,
            "R": 0,
            "SELECT": 0,
            "START": 0
        }
        self.input = input
        self.thread = threading.Thread(target=self.contoller_loop)
        self.thread.daemon = True
        self.thread.start()


if __name__ == '__main__':
    gp = GamePadBase()

    while True:
        print(gp.status)
        time.sleep(50 / 1000.0)