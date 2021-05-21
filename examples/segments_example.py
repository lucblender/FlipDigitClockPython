from flipdigitclock import *
from time import sleep

clock = FlipDigitClock()

clock.clear_digits()

for segment in SEGMENTS:
    for digit in DIGITS:
        clock.set_segment(digit, segment)
        sleep(0.1)

for segment in SEGMENTS:
    for digit in DIGITS:
        clock.reset_segment(digit, segment)
        sleep(0.1)