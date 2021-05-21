from flipdigitclock import *
from datetime import datetime

clock = FlipDigitClock()

start = datetime.now()

while(True):
    delta = datetime.now() - start
    chrono_time = int(str(delta).replace(":","").replace(".","")[:-4])    
    if i%35 == 0:
        clock.set_multiple_digit_number(chrono_time)
    else:
        clock.set_multiple_digit_number(chrono_time, True, True)
    sleep(0.01)