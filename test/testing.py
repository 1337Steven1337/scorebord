from DMD import DMD
from PinLayout import PinLayout
import math
delay = 1
layout = PinLayout(37, 38, 23, 35, 19, 24)
dmd = DMD(1, 1, 32, 16, 1, layout)
displayPixelsWidth = 32
displayPixelsHeight = 16
screen = [0 for x in range(64)]
phase = 0

pixelLookupTable = [
    0x80,  # 0, bit 7
    0x40,  # 1, bit 6
    0x20,  # 2. bit 5
    0x10,  # 3, bit 4
    0x08,  # 4, bit 3
    0x04,  # 5, bit 2
    0x02,  # 6, bit 1
    0x01  # 7, bit 0
]


def pixel_to_bitmap_index(x, y):
    panel = math.floor(int((x/32))) + math.floor(int((y / 16)))
    x = (x % 32) + (panel * 32)
    y = y % 16
    res = x / 8 + (y * 4)
    return int(math.floor(res))


def set_pixel(x, y, on):
    if x >= 32 or y >= 16:
        return
    byte_index = pixel_to_bitmap_index(x, y)
    bit = pixelLookupTable[x & 0x07]
    if not on:
        screen[byte_index] &= ~bit
    else:
        screen[byte_index] |= bit


def get_pixel(x, y):
    byte_index = pixel_to_bitmap_index(x, y)
    bit = pixelLookupTable[x & 0x07]
    try:
        return (screen[byte_index] & bit) > 0
    except:
        print("Requested x,y,got", x, y, byte_index)
        return 0


def print_screen():
    to_print = ""
    for x in range(32*16):
        if (x + 1) % 32 == 0:
            print(to_print)
            to_print = ""
        to_print += str(int(get_pixel(x%32, int(math.floor(x / 32))))) + ", "


def scan():
    global phase
    stride = 4
    stride4 = 16
    for x in range(1):
        offset_pos = (phase + x) * stride
        b0 = screen[offset_pos + 0]
        b1 = screen[offset_pos + stride4]
        b2 = screen[offset_pos + 2 * + stride4]
        b3 = screen[offset_pos + 3 * + stride4]
        print([b3, b2, b1, b0])

    phase = (phase + 1) & 0x03

set_pixel(2, 2, True)


while True:
    for x in range(4):
        scan()
