import pygame
import os
from pygame.locals import *
import time
import RPi.GPIO as GPIO

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setwarnings(False)
# GPIO used for motor A
# GPIO 5 and GPIO 6 are used to control direction
AIN1 = 5
AIN2 = 6
# GPIO 13 is used for PWMA control
PWMA = 13
# GPIO used for motor B
# GPIO 24 and GPIO 25 are used to control direction
BIN1 = 24
BIN2 = 25
# GPIO 18 is used for PWMA control
PWMB = 18

# Set up GPIO
GPIO.setmode(GPIO.BCM)
# 17 is used to switch between motor A and motor B
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 22 is used to let motor run clockwise
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 23 is used to let motor run counterclockwise
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 27 is used to stop the motor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# for motor A
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

# for motor B
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# initialize pygame
pygame.init()

WHITE = 255,255,255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0
screen = pygame.display.set_mode((320,240))

panic_font = pygame.font.Font(None,50)
text_font = pygame.font.Font(None,20)

main_buttons = {'STOP': (160, 120), 'RESUME': (160, 120), 'quit':(280, 200)}
direction_text = ['Stop', 'ClkWise', 'Counter-Clk']
main_buttons_rect = {}

# initialize display histories
queue_A = []
queue_B = []
time_A = []
time_B = []

def initailize_queues():
    queue_A.clear()
    queue_B.clear()
    time_A.clear()
    time_B.clear()

    for i in range(3):
        queue_A.append(direction_text[0])
        queue_B.append(direction_text[0])
        time_A.append(str(0))
        time_B.append(str(0))

    return None

initailize_queues()

# functions to control motor
def clockwise(p, dc, in1, in2, queue, time):
    p.ChangeDutyCycle(dc)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    queue.pop(0)
    queue.append('ClkWise')
    time.pop(0)
    time.append(str(int(time.time() - start_time)))
    return None

def counterclockwise(p, dc, in1, in2,queue,time_q):
    p.ChangeDutyCycle(dc)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in1, GPIO.LOW)
    queue.pop(0)
    queue.append('Counter-Clk')
    time_q.pop(0)
    time_q.append(str(int(time.time() - start_time)))
    return None

def stop(p,queue,time_q):
    p.ChangeDutyCycle(0)
    queue.pop(0)
    queue.append('Stop')
    time_q.pop(0)
    time_q.append(str(0))
    return None

# function to display buttons
def render_button(word, center, font):
    surface = font.render(word, True, WHITE)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)
    main_buttons_rect[button_text] = rect
    return None

# initialize f and duty cycle
frequency = 50
stop_dc = 0
half_dc = 50
full_dc = 100

# initialize pA and pB, the motor should be stopped at initial
pA = GPIO.PWM(PWMA, frequency)
pA.start(0)
pB = GPIO.PWM(PWMB, frequency)
pB.start(0)
p = pA

# get start time
start_time = time.time()

# main part of the rolling control
code_run = True
button_text = 'STOP'
while code_run:
    # initialize the layout
    screen.fill(BLACK)

    # draw the panic circle
    if button_text == 'STOP':
        pygame.draw.circle(screen, RED, (160,120), 50)
    if button_text == 'RESUME':
        pygame.draw.circle(screen, GREEN, (160, 120), 50)

    # display buttons: stop & quit
    render_button(button_text, main_buttons[button_text], panic_font)
    render_button('quit', main_buttons['quit'], panic_font)

    # display direction and time history
    render_button('Left History', (40,50), text_font)
    render_button('Right History', (270,50), text_font)

    for i in range(3):
        render_button(queue_A[i], (20,100+i*20), text_font)
        render_button(time_A[i], (60, 100+i*20), text_font)
        render_button(queue_B[i], (250,100+i*20), text_font)
        render_button(time_B[i], (60, 100 + i * 20), text_font)

    # get events
    for event in pygame.event.get():
        if event.type is MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
        elif event.type is MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            for(my_text,rect) in main_buttons_rect.items():
                if rect.collidepoint(pos):
                    if my_text == 'quit':
                        code_run = False

                    elif my_text=='STOP':
                        stop(pA, queue_A, time_A)
                        stop(pB, queue_B, time_B)
                        initailize_queues()
                        button_text = 'RESUME'

                    elif my_text=='RESUME':
                        button_text = 'STOP'
                        start_time = time.time()

    if not GPIO.input(17):
        if p == pA:
            p = pB
        elif p == pB:
            p = pA

    if not GPIO.input(22):
        if p == pA:
            clockwise(p, half_dc, AIN1, AIN2,queue_A,time_A)
        if p == pB:
            clockwise(p, half_dc, BIN1, BIN2,queue_B,time_B)

    if not GPIO.input(23):
        if p == pA:
            counterclockwise(p, half_dc, AIN1, AIN2, queue_A,time_A)
        if p == pB:
            counterclockwise(p, half_dc, BIN1, BIN2, queue_B,time_B)

    if not GPIO.input(27):
        if p == pA:
            stop(p, queue_A, time_A)
        if p == pB:
            stop(p, queue_B, time_B)


pA.stop()
pB.stop()

GPIO.output(AIN2, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(BIN1, GPIO.LOW)

GPIO.cleanup()
