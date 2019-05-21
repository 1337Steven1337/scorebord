from DMD import DMD
from PinLayout import PinLayout
from random import randint
import time
delay = 1
layout = PinLayout(37, 38, 23, 35, 19, 24)
dmd = DMD(1, 1, 32, 16, 1, layout)
displayStride = 4
screenHeight = 16
displayPixelsHeight = 16
screen = [randint(0, 1) for x in range(128)]

to_print = ""
for x in range(128):
    to_print += " ," + str(int(screen[x]))

print(to_print)
