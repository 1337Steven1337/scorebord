import RPi.GPIO as GPIO
import spidev


class DMDBase(object):
    GPIO.setwarnings(False)
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 250000

    def __init__(self, layout):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(layout.A, GPIO.OUT)
        GPIO.setup(layout.B, GPIO.OUT)
        GPIO.setup(layout.CLK, GPIO.OUT)
        GPIO.setup(layout.STROBE, GPIO.OUT)
        GPIO.setup(layout.DATA, GPIO.OUT)
        GPIO.setup(layout.OE, GPIO.OUT)
        self.layout = layout

    def latch(self):
        self.gpio_out(self.layout.STROBE, 1)
        self.gpio_out(self.layout.STROBE, 0)

    def clock(self):
        self.gpio_out(self.layout.CLK, 1)
        self.gpio_out(self.layout.CLK, 0)

    def transfer_bit(self, bit):
        self.gpio_out(self.layout.DATA, bit)
        self.clock()

    def spi_send(self, byte_array):
        for i in range(len(byte_array)):
            for j in range(7, -1, -1):
                bit = (byte_array[i] & (1 << j)) == 0
                self.transfer_bit(bit)

    def gpio_out(self, pin, value):
        GPIO.output(pin, value)
