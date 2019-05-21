from PinLayout import PinLayout
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
layout = PinLayout(37, 38, 23, 35, 19, 24)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(layout.A, GPIO.OUT)
GPIO.setup(layout.B, GPIO.OUT)
GPIO.setup(layout.CLK, GPIO.OUT)
GPIO.setup(layout.STROBE, GPIO.OUT)
GPIO.setup(layout.DATA, GPIO.OUT)
GPIO.output(layout.DATA, 1)
GPIO.setup(layout.OE, GPIO.OUT)
phase = 0


def transfer_bit(bit):
    gpio_out(layout.DATA, bit)
    gpio_out(layout.CLK, 1)
    gpio_out(layout.CLK, 0)


def gpio_out(pin, value):
    GPIO.output(pin, value)


def scan_full():
    for x in range(4):
        scan()


def scan():
    global phase
    for x in range(0, 64):
        transfer_bit(0)

    gpio_out(layout.OE, 0)
    gpio_out(layout.STROBE, 1)
    gpio_out(layout.STROBE, 0)
    if phase & 0x02:
        gpio_out(layout.B, 1)
    else:
        gpio_out(layout.B, 0)

    if phase & 0x01:
        gpio_out(layout.A, 1)
    else:
        gpio_out(layout.A, 0)
    phase = (phase + 1) & 0x03
    gpio_out(layout.OE, 1)


while True:
    scan_full()
    time.sleep(0.001)
