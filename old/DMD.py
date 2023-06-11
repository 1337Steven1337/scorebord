from DMDBase import DMDBase
import math


class DMD(DMDBase):
    def __init__(self, displayswide, displayshigh, pixelswidth, pixelsheight, layout):
        DMDBase.__init__(self, layout)
        self.displaysWide = displayswide
        self.displaysHigh = displayshigh
        self.displayPixelsWidth = pixelswidth
        self.displayPixelsHeight = pixelsheight
        self.displaysTotal = self.displaysHigh * self.displaysWide
        self.screenWidth = self.displayPixelsWidth * self.displaysWide
        self.screenHeight = self.displayPixelsHeight * self.displaysHigh
        self.screen = [0 for x in range(self.displaysTotal * 64)]
        self.phase = 0
        self.row_size = self.displaysTotal << 2
        self.row3 = ((self.displaysTotal << 2) * 3) << 2
        self.row2 = self.displaysTotal << 5
        self.row1 = self.displaysTotal << 4

    def pixel_to_bitmap_index(self, x, y):
        panel = int(math.floor((x / self.displayPixelsWidth))) + int(math.floor((self.displaysWide * (y / self.displayPixelsHeight))))
        x = (x % self.displayPixelsWidth) + (panel * self.displayPixelsWidth)
        y = y % self.displayPixelsHeight
        res = x / 8 + y * (self.displaysTotal << 2)
        return int(math.floor(res))


    def set_pixel(self, x, y):
        if x >= self.screenWidth or y >= self.screenHeight:
            return
        byte_index = self.pixel_to_bitmap_index(x, y)
        bit = super(DMD, self).pixelLookupTable[x & 0x07]
        self.screen[byte_index] |= bit

    def scan_full(self):
        for x in range(4):
            self.scan()

    def scan(self):
        offset = self.row_size * self.phase
        for x in range(self.row_size):
            off_pos = offset + x
            b3 = self.screen[off_pos + self.row3]
            b2 = self.screen[off_pos + self.row2]
            b1 = self.screen[off_pos + self.row1]
            b0 = self.screen[off_pos + 0]
            super(DMD, self).spi_send([b3,b2,b1,b0])

        super(DMD, self).gpio_out(self.layout.OE, 0)
        super(DMD, self).latch()
        super(DMD, self).gpio_out(self.layout.A, self.phase & 0x01)
        super(DMD, self).gpio_out(self.layout.B, self.phase & 0x02)
        self.phase = (self.phase + 1) % 4
        super(DMD, self).gpio_out(self.layout.OE, 1)

    def draw_line(self, x1, y1, x2, y2):
        dy = y2 - y1
        dx = x2 - x1
        stepy = 1
        stepx = 1
        if dy < 0:
            dy = -dy
            stepy = -1
        if dx < 0:
            dx = -dx
            stepx = -1
        dy *= 2
        dx *= 2
        self.set_pixel(x1, y1)
        if dx > dy:
            fraction = dy - dx / 2
            while x1 is not x2:
                if fraction >= 0:
                    y1 += stepy
                    fraction -= dx
                x1 += stepx
                fraction += dy
                self.set_pixel(x1, y1)
        else:
            fraction = dx - dy / 2
            while y1 is not y2:
                if fraction >= 0:
                    x1 += stepx
                    fraction -= dy
                y1 += stepy
                fraction += dx
                self.set_pixel(x1, y1)
