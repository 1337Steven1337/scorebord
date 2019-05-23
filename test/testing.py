from DMD import DMD
from PinLayout import PinLayout
from random import randint
import math
delay = 1
layout = PinLayout(37, 38, 23, 35, 19, 24)
dmd = DMD(1, 1, 32, 16, 1, layout)
displayPixelsWidth = 32
displayPixelsHeight = 16
screen = [0 for x in range(64)]

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
        print("Requested x,y,got",x,y ,byte_index)
        return 0



def print_screen():
    to_print = ""
    for x in range(32*16):
        if (x + 1) % 32 == 0:
            print(to_print)
            to_print = ""
        to_print += str(int(get_pixel(x%32, int(math.floor(x / 32))))) + ", "


for x in range(16):
    set_pixel(x, x, True)

print_screen()
