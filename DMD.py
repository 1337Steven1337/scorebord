from DMDBase import DMDBase
from GraphicsMode import GraphicsMode as graphicsmode
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
        self.displayStrideWidth = int(math.floor((self.screenWidth + 7) / 8))
        self.screen_size_bytes = self.displayStrideWidth * self.screenHeight
        self.screen = [0 for x in range(self.displaysTotal * self.screen_size_bytes)]
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

    def set_pixel(self, x, y, mode):
        if x >= self.screenWidth or y >= self.screenHeight:
            return
        byte_index = self.pixel_to_bitmap_index(x, y)
        bit = super(DMD, self).pixelLookupTable[x & 0x07]
        if mode == graphicsmode.ON:
            self.screen[byte_index] &= ~bit
        elif mode == graphicsmode.OFF:
            self.screen[byte_index] |= bit
        elif mode == graphicsmode.OR:
            self.screen[byte_index] = ~(~self.screen[byte_index] | bit)
        elif mode == graphicsmode.NOR:
            self.screen[byte_index] = (~self.screen[byte_index] | bit)
        elif mode == graphicsmode.XOR:
            self.screen[byte_index] ^= bit

    def get_pixel(self, x, y):
        byte_index = self.pixel_to_bitmap_index(x, y)
        bit = super(DMD, self).pixelLookupTable[x & 0x07]
        return (self.screen[byte_index] & bit) > 0

    def print_screen(self):
        to_print = ""
        for x in range(self.screenWidth * self.screenHeight):
            if x is not 0 and x % 32 == 0:
                print(to_print)
                to_print = ""
            to_print += str(int(self.get_pixel(x % self.displayPixelsWidth, int(math.floor(x / self.displayPixelsWidth))))) + ", "

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
            super(DMD, self).spi_send([b3, b2, b1, b0])

        super(DMD, self).gpio_out(self.layout.OE, 0)
        super(DMD, self).latch()
        super(DMD, self).gpio_out(self.layout.A, self.phase & 0x01)
        super(DMD, self).gpio_out(self.layout.B, self.phase & 0x02)
        self.phase = (self.phase + 1) % 4
        super(DMD, self).gpio_out(self.layout.OE, 1)

    def clear_screen(self):
        self.screen = [0 for x in range(self.displaysTotal * self.screen_size_bytes)]

    def fill_screen(self):
        self.screen = [255 for x in range(self.displaysTotal * self.screen_size_bytes)]

    def draw_line(self, x1, y1, x2, y2, mode):
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
        self.set_pixel(x1, y2, mode)
        if dx > dy:
            fraction = dy - dx / 2
            while x1 is not x2:
                if fraction >= 0:
                    y1 += stepy
                    fraction -= dx
                x1 += stepx
                fraction += dy
                self.set_pixel(x1, y1, mode)
        else:
            fraction = dx - dy / 2
            while y1 is not y2:
                if fraction >= 0:
                    x1 += stepx
                    fraction -= dy
                y1 += stepy
                fraction += dx
                self.set_pixel(x1, y1, mode)

    def draw_circle(self, xcenter, ycenter, radius, mode):
        x = -radius
        y = 0
        error = 2 - 2 * radius
        while x < 0:
            self.set_pixel(xcenter - x, ycenter + y, mode)
            self.set_pixel(xcenter - y, ycenter - x, mode)
            self.set_pixel(xcenter + x, ycenter - y, mode)
            self.set_pixel(xcenter + y, ycenter + x, mode)
            radius = error
            if radius <= y:
                y += 1
                error += y * 2 + 1
            if radius > x or error > y:
                x += 1
                error += x * 2 + 1

    def draw_box(self, x1, y1, x2, y2, mode):
        self.draw_line(x1, y1, x2, y1, mode)
        self.draw_line(x2, y1, x2, y2, mode)
        self.draw_line(x2, y2, x1, y2, mode)
        self.draw_line(x1, y2, x1, y1, mode)

    def draw_filled_box(self, x1, y1, x2, y2, mode):
        for x in range(x1,x2 + 1):
            self.draw_line(x, y1 - 1, x, y2, mode)

