import RPi.GPIO as GPIO


class DMDBase(object):
    GPIO.setwarnings(False)

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
    def __init__(self, layout):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(layout.A, GPIO.OUT)
        GPIO.setup(layout.B, GPIO.OUT)
        GPIO.setup(layout.CLK, GPIO.OUT)
        GPIO.setup(layout.STROBE, GPIO.OUT)
        GPIO.setup(layout.OE, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        self.layout = layout

    def latch(self):
        self.gpio_out(self.layout.STROBE, 1)
        self.gpio_out(self.layout.STROBE, 0)

    def clock(self):
        self.gpio_out(self.layout.CLK, 1)
        self.gpio_out(self.layout.CLK, 0)

    def transfer_byte(self, byte):
	    self.gpio_out(7, byte)
        self.clock()

    def spi_send(self, byte_array):
        for i in range(len(byte_array)):
	    for j in range(8):
		self.transfer_byte((byte_array[i] & (1 << 7)) == 0)
		byte_array[i] <<= 1

    def gpio_out(self, pin, value):
        GPIO.output(pin, value)

