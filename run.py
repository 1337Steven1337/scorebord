from DMD import DMD
from PinLayout import PinLayout
from random import randint
import threading

delay = 0.000001
layout = PinLayout(37, 38, 23, 35, 19, 24)
dmd = DMD(1, 1, 32, 16, layout)


def random_pixel(update):
        if not update.is_set():
            threading.Timer(1, random_pixel,[update]).start()
        dmd.clear()
        for x in range(50):
                dmd.set_pixel(randint(0,32), randint(0,16), True)


def update_screen(running):
    dmd.scan_full()
    if not running.is_set():
        threading.Timer(delay, update_screen, [running]).start()


update = threading.Event()
random_pixel(update)
running = threading.Event()
update_screen(running)

