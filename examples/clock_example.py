from flipdigitclock import *
from datetime import datetime

clock = FlipDigitClock()

while(True):
    now = datetime.now()
    current_time = int(now.strftime("%H%M%S"))
    if i%5 == 0:
        clock.set_multiple_digit_number(current_time)
    else:
        clock.set_multiple_digit_number(current_time, True, True)
    sleep(0.1)
