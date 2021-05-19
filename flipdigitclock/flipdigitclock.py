import RPi.GPIO as GPIO
from time import sleep


number_segments = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]

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


SEMI_COLLON_4 = 3
SEMI_COLLON_2 = 7
DIGIT_1 = 5
DIGIT_2 = 1
DIGIT_3 = 6
DIGIT_4 = 2
DIGIT_5 = 4
DIGIT_6 = 0

DIGITS = [DIGIT_1, DIGIT_2, DIGIT_3, DIGIT_4, DIGIT_5, DIGIT_6, SEMI_COLLON_2, SEMI_COLLON_4]

SEGMENT_A = 3
SEGMENT_B = 5
SEGMENT_C = 1
SEGMENT_D = 6
SEGMENT_E = 2
SEGMENT_F = 4
SEGMENT_G = 0
COLLON = 7

SEGMENTS = [SEGMENT_A, SEGMENT_B, SEGMENT_C, SEGMENT_D, SEGMENT_E, SEGMENT_F, SEGMENT_G, COLLON]

A_DIG = 7
B_DIG = 5
C_DIG = 6
SET_DIG_EN = 12
RES_DIG_EN = 13

A_SEG = 19
B_SEG = 16
C_SEG = 26
SET_SEG_EN = 20
RES_SEG_EN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_DIG,       GPIO.OUT)
GPIO.setup(B_DIG,       GPIO.OUT)
GPIO.setup(C_DIG,       GPIO.OUT)
GPIO.setup(SET_DIG_EN,  GPIO.OUT)
GPIO.setup(RES_DIG_EN,  GPIO.OUT)

GPIO.setup(A_SEG,       GPIO.OUT)
GPIO.setup(B_SEG,       GPIO.OUT)
GPIO.setup(C_SEG,       GPIO.OUT)
GPIO.setup(SET_SEG_EN,  GPIO.OUT)
GPIO.setup(RES_SEG_EN,  GPIO.OUT)

def reset_segment(digit, seg):
    digit_num = bin_to_GPIO_level(digit)
    segment = bin_to_GPIO_level(seg)
    GPIO.output(A_DIG,      digit_num[0])
    GPIO.output(B_DIG,      digit_num[1])
    GPIO.output(C_DIG,      digit_num[2])
    GPIO.output(SET_DIG_EN, GPIO.HIGH)
    GPIO.output(RES_DIG_EN, GPIO.LOW) 
    sleep(0.001)
    GPIO.output(A_SEG,      segment[0])
    GPIO.output(B_SEG,      segment[1])
    GPIO.output(C_SEG,      segment[2])
    GPIO.output(SET_SEG_EN, GPIO.LOW)
    GPIO.output(RES_SEG_EN, GPIO.HIGH)
    sleep(0.001)
    reset_all()

def set_segment(digit, seg):
    digit_num = bin_to_GPIO_level(digit)
    segment = bin_to_GPIO_level(seg)
    GPIO.output(A_DIG,      digit_num[0])
    GPIO.output(B_DIG,      digit_num[1])
    GPIO.output(C_DIG,      digit_num[2])
    GPIO.output(SET_DIG_EN, GPIO.LOW)
    GPIO.output(RES_DIG_EN, GPIO.HIGH)  
    sleep(0.001)  
    GPIO.output(A_SEG,      segment[0])
    GPIO.output(B_SEG,      segment[1])
    GPIO.output(C_SEG,      segment[2])
    GPIO.output(SET_SEG_EN, GPIO.HIGH)
    GPIO.output(RES_SEG_EN, GPIO.LOW)
    sleep(0.001)
    reset_all()

def set_number(digit, number):
    hex_code = bin_to_set_reset_segment(number_segments[number])
    i = 0
    for bin_code in hex_code:
        if bin_code == 0:
            reset_segment(digit, SEGMENTS[i])
        else:
            set_segment(digit, SEGMENTS[i])
        i += 1

def clear_digit(digit,):
    for i in range(0,8):
        reset_segment(digit, i)
   
def set_multiple_digit_number(num, dot_first = False, dot_second = False):
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
        set_number(DIGITS[i],pos_nums[i])
    if dot_first == True:
        set_segment(SEMI_COLLON_2, COLLON)
    else:
        reset_segment(SEMI_COLLON_2, COLLON)
    if dot_second == True:
        set_segment(SEMI_COLLON_4, COLLON)
    else:
        reset_segment(SEMI_COLLON_4, COLLON)
        

def reset_all():
    GPIO.output(A_DIG,      GPIO.LOW)
    GPIO.output(B_DIG,      GPIO.LOW)
    GPIO.output(C_DIG,      GPIO.LOW)
    GPIO.output(SET_DIG_EN, GPIO.LOW)
    GPIO.output(RES_DIG_EN, GPIO.LOW)
    GPIO.output(A_SEG,      GPIO.LOW)
    GPIO.output(B_SEG,      GPIO.LOW)
    GPIO.output(C_SEG,      GPIO.LOW)
    GPIO.output(SET_SEG_EN, GPIO.LOW)
    GPIO.output(RES_SEG_EN, GPIO.LOW)



