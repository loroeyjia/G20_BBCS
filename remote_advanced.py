import radio
import random
from microbit import *

CONTROL_CHARS = 'ABCDEFG'
CONTROL_CHAR = '-'

class Servo:

    """
    A simple class for controlling hobby servos.

    Args:
        pin (pin0 .. pin3): The pin where servo is connected.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between minimum and maximum positions.

    Usage:
        SG90 @ 3.3v servo connected to pin0
        = Servo(pin0).write_angle(90)
    """

    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
        self.pin.write_digital(0)  # turn the pin off

    def write_angle(self, degrees=None):
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)
        
radio.on()

while True:
    try:
        if button_b.is_pressed():
            CONTROL_CHAR = random.choice(CONTROL_CHARS)
            display.show(CONTROL_CHAR)
            radio.send('pair' + CONTROL_CHAR)
            sleep(100)
        else:
            incoming = radio.receive()
            if incoming and incoming.startswith('control' + CONTROL_CHAR):
                raw = float(incoming[8:])
                reading = raw/204
                if reading > 4.0:
                    pos = 4
                elif reading > 3.0:
                    pos = 3
                elif reading > 2.0:
                    pos = 2
                elif reading > 1.0:
                    pos = 1
                else:
                    pos = 0

                columns = ['0' for i in range(5)] 
                columns[pos] = '9'
                img = ((''.join(columns) + ':')*5)[0:-1]
                img = Image(img)
                display.show(img)
                Servo(pin0).write_angle(raw/1023*179)
    except:
        radio.off()
        radio.on()