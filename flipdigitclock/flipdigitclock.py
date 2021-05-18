import RPi.GPIO as GPIO
from time import sleep

def bin_to_GPIO_level(to_convert):
    to_return = []
    binary = bin(to_convert).replace('0b','').rjust(3,'0')
    for bit in binary:
        if bit == '1':
            to_return.append(GPIO.HIGH)
        else:
            to_return.append(GPIO.LOW)
    return to_return
        

SEMI_COLLON_4 = 7
SEMI_COLLON_2 = 3
DIGIT_1 = 0
DIGIT_2 = 4
DIGIT_3 = 2
DIGIT_4 = 6
DIGIT_5 = 1
DIGIT_6 = 5

DIGITS = [DIGIT_1, DIGIT_2, DIGIT_3, DIGIT_4, DIGIT_5, DIGIT_6, SEMI_COLLON_2, SEMI_COLLON_4]

SEGMENT_A = 3
SEGMENT_B = 1
SEGMENT_C = 5
SEGMENT_D = 0
SEGMENT_E = 4
SEGMENT_F = 2
SEGMENT_G = 6
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

for digit in DIGITS:
    for segment in SEGMENTS:
        set_segment(digit, segment)
    sleep(1)
    
    
set_segment(COLLON, SEMI_COLLON_4)

