from DMD import DMD
from PinLayout import PinLayout
import time
delay = 0.3
layout = PinLayout(37, 38, 23, 35, 19, 24)
dmd = DMD(1, 1, 32, 16, layout)

for x in range(16):
    dmd.set_pixel(x, x, True)

dmd.print_screen()

while True:
    dmd.scan_full()
    time.sleep(delay)
