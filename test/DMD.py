import math

class DMD(object):
    displayPixelsWidth = 32
    displayPixelsHeight = 16
    displayBitsPerPixel = 1
    displaysWide = 1
    displaysHigh = 1
    displaysTotal = 1
    bDMDByte = 0
    screen = []

    pixelLookupTable = [
           0x80,   # 0, bit 7
           0x40,   # 1, bit 6
           0x20,   # 2. bit 5
           0x10,   # 3, bit 4
           0x08,   # 4, bit 3
           0x04,   # 5, bit 2
           0x02,   # 6, bit 1
           0x01    # 7, bit 0
    ]

    def __init__(self, displayswide, displayshigh, pixelswidth, pixelsheight, bpp, layout):
        self.displaysWide = displayswide
        self.displaysHigh = displayshigh
        self.displayPixelsWidth = pixelswidth
        self.displayPixelsHeight = pixelsheight
        self.displayBitsPerPixel = bpp

        self.displaysTotal = self.displaysHigh * self.displaysWide
        self.row1 = self.displaysTotal << 4
        self.row2 = self.displaysTotal << 5
        self.row3 = ((self.displaysTotal << 2) * 3) << 2
        self.screen = [0 for x in range((self.displaysWide * self.displayPixelsWidth) * (self.displaysHigh * self.displayPixelsHeight))]
        self.displayStride = math.floor((self.displayPixelsWidth * self.displaysWide + 7) / 8)

    def clear(self):
        for x in range(len(self.screen)):
            self.screen[x] = 0

    def set_pixel(self, x, y, invert_mode=False, pixel=False):
        if x < 0 or x >= self.displayPixelsWidth * self.displaysWide:
            return
        if y < 0 or y >= self.displayPixelsHeight * self.displaysHigh:
            return
        panel = (x / self.displayPixelsWidth) + (self.displaysWide * (y / self.displayPixelsHeight))
        x = (x % self.displayPixelsWidth) + panel << 5
        y = y % self.displayPixelsHeight
        screen_pointer = x / 8 + y * (self.displaysTotal << 2)
        lookup = self.pixelLookupTable[x & 0x07]
        if invert_mode:
            if pixel:
                self.screen[screen_pointer] |= lookup  # one bit is pixel off
            else:
                self.screen[screen_pointer] &= ~lookup  # zero bit is pixel on
        else:
            if pixel:
                self.screen[screen_pointer] &= ~lookup  # zero bit is pixel on
            else:
                self.screen[screen_pointer] |= lookup  # one bit is pixel off

    def scan_full(self):
        for x in range(4):
            self.scan()

    def scan(self):
        row_size = self.displaysTotal << 2
        offset = row_size * self.bDMDByte
        for x in range(row_size):
            offset_pos = offset + x
            b3 = self.screen[offset_pos + self.row3]
            b2 = self.screen[offset_pos + self.row2]
            b1 = self.screen[offset_pos + self.row1]
            b0 = self.screen[offset_pos + 0]
            print([b3, b2, b1, b0])
