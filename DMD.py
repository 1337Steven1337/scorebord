from DMDBase import DMDBase
import math


class DMD(DMDBase):
    displayPixelsWidth = 32
    displayPixelsHeight = 16
    displayBitsPerPixel = 1
    displayStrideWidth = 0
    displaysWide = 1
    displaysHigh = 1
    displaysTotal = 1
    phase = 0
    screen_size = 0
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
        DMDBase.__init__(self, layout)
        self.displaysWide = displayswide
        self.displaysHigh = displayshigh
        self.displayPixelsWidth = pixelswidth
        self.displayPixelsHeight = pixelsheight
        self.displayBitsPerPixel = bpp
        self.displaysTotal = self.displaysHigh * self.displaysWide
        self.screenWidth = self.displayPixelsWidth * self.displaysWide
        self.screenHeight = self.displayPixelsHeight * self.displaysHigh
        self.displayStrideWidth = int(math.floor((self.screenWidth + 7) / 8))
        self.displayStrideHeight = int(math.floor((self.screenHeight + self.displayPixelsHeight - 1) / self.displayPixelsHeight))
        self.screen_size = self.displayStrideWidth * self.screenHeight
        self.screen = [0 for x in range(self.displaysTotal * self.screen_size)]

    def pixel_to_bitmap_index(self, x, y):
        panel = int(math.floor((x / self.displayPixelsWidth))) + int(math.floor((self.displaysWide * (y / self.displayPixelsHeight))))
        x = (x % self.displayPixelsWidth) + (panel * self.displayPixelsWidth)
        y = y % self.displayPixelsHeight
        res = x / 8 + y * (self.displaysTotal << 2)
        return int(math.floor(res))

    def set_pixel(self, x, y, on):
        if x >= self.screenWidth or y >= self.screenHeight:
            return
        byte_index = self.pixel_to_bitmap_index(x, y)
        bit = self.pixelLookupTable[x & 0x07]
        if not on:
            self.screen[byte_index] &= ~bit
        else:
            self.screen[byte_index] |= bit

    def get_pixel(self, x, y):
        byte_index = self.pixel_to_bitmap_index(x, y)
        bit = self.pixelLookupTable[x & 0x07]
        return (self.screen[byte_index] & bit) > 0

    def print_screen(self):
        to_print = ""
        for x in range(self.screenWidth * self.screenHeight):
            if (x + 1) % 32 == 0:
                print(to_print)
                to_print = ""
            to_print += str(int(self.get_pixel(x % self.displayPixelsWidth, int(math.floor(x / self.displayPixelsWidth))))) + ", "

    def scan_full(self):
        for x in range(4):
            self.scan()

    def scan(self):
        row_size = self.displayStrideWidth * self.displayStrideHeight
        for x in range(row_size):
            b0 = self.screen[(self.phase + 0) * row_size]
            b1 = self.screen[(self.phase + 4) * row_size]
            b2 = self.screen[(self.phase + 8) * row_size]
            b3 = self.screen[(self.phase + 12) * row_size]
            super(DMD, self).spi_send([b3, b2, b1, b0])

        super(DMD, self).gpio_out(self.layout.OE, 0)
        super(DMD, self).latch()
        if self.phase & 0x02:
            super(DMD, self).gpio_out(self.layout.B, 1)
        else:
            super(DMD, self).gpio_out(self.layout.B, 0)
        if self.phase & 0x01:
            super(DMD, self).gpio_out(self.layout.A, 1)
        else:
            super(DMD, self).gpio_out(self.layout.A, 0)

        self.phase = (self.phase + 1) & 0x03
        super(DMD, self).gpio_out(self.layout.OE, 1)


