from DMD import DMD
from PinLayout import PinLayout

layout = PinLayout(37, 38, 23, 35, 24)
dmd = DMD(7, 1, 32, 16, layout)

dmd.draw_line(0,0,223,15)
dmd.draw_line(0,15,223,0)

while True:
    dmd.scan_full()
