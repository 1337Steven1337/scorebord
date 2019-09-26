class PinLayout(object):
    OE = 24
    A = 39
    B = 40
    CLK = 23  # CLOCK [CLK]
    STROBE = 37  # [SLCK] [LATCH] [STROBE]

    def __init__(self, a, b, clk, latch, oe):
        self.A = a
        self.B = b
        self.CLK = clk
        self.STROBE = latch
        self.OE = oe
