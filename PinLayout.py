class PinLayout(object):
    OE = 24
    A = 37
    B = 38
    CLK = 23  # CLOCK [CLK]
    STROBE = 35  # [SLCK] [LATCH] [STROBE]
    DATA = 19  # DATA

    def __init__(self, a, b, clk, latch, data, oe):
        self.A = a
        self.B = b
        self.CLK = clk
        self.STROBE = latch
        self.DATA = data
        self.OE = oe