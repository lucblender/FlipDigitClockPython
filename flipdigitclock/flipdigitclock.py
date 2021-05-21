import RPi.GPIO as GPIO
from time import sleep, time
from enum import Enum
import signal
import sys

number_segments = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]

class DigitNumber(Enum):
    SEMI_COLLON_2 = 7
    SEMI_COLLON_1 = 3
    DIGIT_1 = 5
    DIGIT_2 = 1
    DIGIT_3 = 6
    DIGIT_4 = 2
    DIGIT_5 = 4
    DIGIT_6 = 0

DIGITS = [DigitNumber.DIGIT_1.value, DigitNumber.DIGIT_2.value, DigitNumber.DIGIT_3.value, DigitNumber.DIGIT_4.value, DigitNumber.DIGIT_5.value, DigitNumber.DIGIT_6.value, DigitNumber.SEMI_COLLON_1.value, DigitNumber.SEMI_COLLON_2.value]

class SegmentName(Enum):
    A = 3
    B = 5
    C = 1
    D = 6
    E = 2
    F = 4
    G = 0
    COLLON = 7

SEGMENTS = [SegmentName.A.value, SegmentName.B.value, SegmentName.C.value, SegmentName.D.value, SegmentName.E.value, SegmentName.F.value, SegmentName.G.value, SegmentName.COLLON.value]

def bin_to_GPIO_level(to_convert):
    to_return = []
    binary = bin(to_convert).replace('0b','').rjust(3,'0')
    for bit in binary:
        if bit == '1':
            to_return.append(GPIO.HIGH)
        else:
            to_return.append(GPIO.LOW)
    return to_return

def bin_to_set_reset_segment(to_convert):
    to_return = []
    binary = bin(to_convert).replace('0b','').rjust(7,'0')
    for bit in binary:
        if bit == '1':
            to_return.append(1)
        else:
            to_return.append(0)
    return to_return

class FlipDigitClock:
    
    def __init__(self, A_DIG = 25, B_DIG = 5, C_DIG = 6, SET_DIG_EN = 12, RES_DIG_EN = 13, A_SEG = 19, B_SEG = 16, C_SEG = 26, SET_SEG_EN = 20, RES_SEG_EN = 21):
        self.__A_DIG = A_DIG
        self.__B_DIG = B_DIG
        self.__C_DIG = C_DIG
        self.__SET_DIG_EN = SET_DIG_EN
        self.__RES_DIG_EN = RES_DIG_EN
        
        self.__A_SEG = A_SEG
        self.__B_SEG = B_SEG
        self.__C_SEG = C_SEG
        self.__SET_SEG_EN = SET_SEG_EN
        self.__RES_SEG_EN = RES_SEG_EN
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__A_DIG,       GPIO.OUT)
        GPIO.setup(self.__B_DIG,       GPIO.OUT)
        GPIO.setup(self.__C_DIG,       GPIO.OUT)
        GPIO.setup(self.__SET_DIG_EN,  GPIO.OUT)
        GPIO.setup(self.__RES_DIG_EN,  GPIO.OUT)
        
        GPIO.setup(self.__A_SEG,       GPIO.OUT)
        GPIO.setup(self.__B_SEG,       GPIO.OUT)
        GPIO.setup(self.__C_SEG,       GPIO.OUT)
        GPIO.setup(self.__SET_SEG_EN,  GPIO.OUT)
        GPIO.setup(self.__RES_SEG_EN,  GPIO.OUT)
        self.reset_all()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTSTP, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        self.reset_all()
        GPIO.cleanup()
        print("FlipDigitClock exited properly, GPIOs reset in safe state")
        sys.exit(0)
    
    def reset_segment(self, digit, seg):
        digit_num = bin_to_GPIO_level(digit)
        segment = bin_to_GPIO_level(seg)
        GPIO.output(self.__A_DIG,      digit_num[0])
        GPIO.output(self.__B_DIG,      digit_num[1])
        GPIO.output(self.__C_DIG,      digit_num[2])
        GPIO.output(self.__SET_DIG_EN, GPIO.HIGH)
        GPIO.output(self.__RES_DIG_EN, GPIO.LOW) 
        sleep(0.0001)
        GPIO.output(self.__A_SEG,      segment[0])
        GPIO.output(self.__B_SEG,      segment[1])
        GPIO.output(self.__C_SEG,      segment[2])
        GPIO.output(self.__SET_SEG_EN, GPIO.LOW)
        GPIO.output(self.__RES_SEG_EN, GPIO.HIGH)
        sleep(0.0001)
        self.reset_all()
    
    def set_segment(self, digit, seg):
        digit_num = bin_to_GPIO_level(digit)
        segment = bin_to_GPIO_level(seg)
        GPIO.output(self.__A_DIG,      digit_num[0])
        GPIO.output(self.__B_DIG,      digit_num[1])
        GPIO.output(self.__C_DIG,      digit_num[2])
        GPIO.output(self.__SET_DIG_EN, GPIO.LOW)
        GPIO.output(self.__RES_DIG_EN, GPIO.HIGH)  
        sleep(0.0001)  
        GPIO.output(self.__A_SEG,      segment[0])
        GPIO.output(self.__B_SEG,      segment[1])
        GPIO.output(self.__C_SEG,      segment[2])
        GPIO.output(self.__SET_SEG_EN, GPIO.HIGH)
        GPIO.output(self.__RES_SEG_EN, GPIO.LOW)
        sleep(0.0001)
        self.reset_all()
    
    def set_segments(self, digit, hex_segment):
        hex_code = bin_to_set_reset_segment(hex_segment)
        i = 0
        for bin_code in hex_code:
            if bin_code == 0:
                self.reset_segment(digit, SEGMENTS[i])
            else:
                self.set_segment(digit, SEGMENTS[i])
            i += 1
    
    def clear_digit(self, digit):
        for i in range(0,8):
            self.reset_segment(digit, i)
    
    def clear_digits(self):
        for i in range(0,6):
            self.clear_digit(DIGITS[i])
        self.reset_segment(DigitNumber.SEMI_COLLON_2.value, SegmentName.COLLON.value)
        self.reset_segment(DigitNumber.SEMI_COLLON_1.value, SegmentName.COLLON.value)
    
    def set_number(self, digit, number):
        self.set_segments(digit, number_segments[number])
    
    def set_dots(self, dot_first, dot_second):
        if dot_first == True:
            self.set_segment(DigitNumber.SEMI_COLLON_1.value, SegmentName.COLLON.value)
        else:
            self.reset_segment(DigitNumber.SEMI_COLLON_1.value, SegmentName.COLLON.value)
        if dot_second == True:
            self.set_segment(DigitNumber.SEMI_COLLON_2.value, SegmentName.COLLON.value)
        else:
            self.reset_segment(DigitNumber.SEMI_COLLON_2.value, SegmentName.COLLON.value)
    
    def set_multiple_digit_number(self, num, dot_first = False, dot_second = False):
        sign = 1 if num < 0 else 0
        num = abs(num)
        pos_nums = []
        while num != 0:
            pos_nums.append(num % 10)
            num = num // 10
        pos_nums = pos_nums[:6]
        if len(pos_nums) < 6:        
            pos_nums = pos_nums+[0]*(6-len(pos_nums))        
        for i in range(0,6):
            self.set_number(DIGITS[i],pos_nums[i])
        self.set_dots(dot_first, dot_second)
    
    def reset_all(self):
        GPIO.output(self.__A_DIG,      GPIO.LOW)
        GPIO.output(self.__B_DIG,      GPIO.LOW)
        GPIO.output(self.__C_DIG,      GPIO.LOW)
        GPIO.output(self.__SET_DIG_EN, GPIO.LOW)
        GPIO.output(self.__RES_DIG_EN, GPIO.LOW)
        GPIO.output(self.__A_SEG,      GPIO.LOW)
        GPIO.output(self.__B_SEG,      GPIO.LOW)
        GPIO.output(self.__C_SEG,      GPIO.LOW)
        GPIO.output(self.__SET_SEG_EN, GPIO.LOW)
        GPIO.output(self.__RES_SEG_EN, GPIO.LOW)
