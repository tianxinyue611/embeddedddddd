import pygame
import os
from pygame.locals import *
import time
import RPi.GPIO as GPIO

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

# initialize pygame
pygame.init()

#GPIO.setwarnings(False)
# GPIO used for motor A
# GPIO 5 and GPIO 6 are used to control direction
AIN1 = 5
AIN2 = 6
# GPIO 13 is used for PWMA control
PWMA = 13
# GPIO used for motor B
# GPIO 20 and GPIO 21 are used to control direction
BIN1 = 20
BIN2 = 21
# GPIO 12 is used for PWMA control
PWMB = 12

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


WHITE = 255,255,255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0
screen = pygame.display.set_mode((320,240))

panic_font = pygame.font.Font(None,50)
text_font = pygame.font.Font(None,20)

main_buttons = {'STOP': (160, 120), 'RESUME': (160, 120), 'quit':(280, 200),'start':(100,200)}
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
def clockwise(p, dc, in1, in2, queue, time_q):
    p.ChangeDutyCycle(dc)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    queue.pop(0)
    queue.append('ClkWise')
    time_q.pop(0)
    time_q.append(str(int(time.time() - start_time)))
    return None

def counterclockwise(p, dc, in1, in2,queue,time_q):
    p.ChangeDutyCycle(dc)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
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
    time_q.append(str(int(time.time() - start_time)))
    return None

# function to display buttons
def render_button(word, center, font):
    global screen
    f_surface = font.render(word, True, WHITE)
    rect = f_surface.get_rect(center=center)
    screen.blit(f_surface, rect)
    main_buttons_rect[word] = rect
    return None



# initialize f and duty cycle
frequency = 50
stop_dc = 0
half_dc = 50
full_dc = 100
past_state = 'stop'
# initialize pA and pB, the motor should be stopped at initial
pA = GPIO.PWM(PWMA, frequency)
pA.start(0)
pB = GPIO.PWM(PWMB, frequency)
pB.start(0)
p = pB
flag = 1
# get start time


# main part of the rolling control
code_run = True
start = False
button_text = 'STOP'
time_start = time.time()
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
    render_button('start', main_buttons['start'], panic_font)
    
    
 

    # display direction and time history
    render_button('Left History', (40,50), text_font)
    render_button('Right History', (270,50), text_font)

    
    for i in range(3):
        render_button(queue_A[i], (20,100+i*20), text_font)
        render_button(time_A[i], (60, 100+i*20), text_font)
        render_button(queue_B[i], (250,100+i*20), text_font)
        render_button(time_B[i], (300, 100 + i * 20), text_font)
        
    
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
                        
                    if my_text == 'start':
                        start = True
                        start_time = time.time()
                        current_state = "forward"
                        '''
                        while start:
                            clockwise(pA, full_dc, AIN1, AIN2,queue_A,time_A)
                            clockwise(pB, full_dc, BIN1, BIN2,queue_B,time_B)
                            time.sleep(3)
                            stop(pA, queue_A, time_A)
                            stop(pB, queue_B, time_B)
                            time.sleep(2)
                            counterclockwise(pA, full_dc, AIN1, AIN2, queue_A,time_A)
                            counterclockwise(pB, full_dc, BIN1, BIN2, queue_B,time_B)
                            time.sleep(3)
                            stop(pA, queue_A, time_A)
                            stop(pB, queue_B, time_B)
                            time.sleep(2)
                            clockwise(pA, full_dc, AIN1, AIN2,queue_A,time_A)
                            clockwise(pB, half_dc, BIN1, BIN2,queue_B,time_B)
                            time.sleep(3)
                            stop(pA, queue_A, time_A)
                            stop(pB, queue_B, time_B)
                            time.sleep(2)
                            clockwise(pA, half_dc, AIN1, AIN2,queue_A,time_A)
                            clockwise(pB, full_dc, BIN1, BIN2,queue_B,time_B)
                            time.sleep(3)
                            stop(pA, queue_A, time_A)
                            stop(pB, queue_B, time_B)
                            time.sleep(2)
                            
                         
                                
                                
                            if not GPIO.input(27):
                                time.sleep(0.4)
                                start = False
                                code_run = False
                           '''     
                                                 
                           
                        

                    if my_text=='STOP':
                        print("stop")
                        stop(pA, queue_A, time_A)
                        stop(pB, queue_B, time_B)
                        
                        flag = 0
                        #time.sleep(0.5)
                        button_text = 'RESUME'
                        #stop(pA, queue_A, time_A)
                        #stop(pB, queue_B, time_B)
                        #initailize_queues()
                        #button_text = 'RESUME'
                        
                    elif my_text=='RESUME':
                        print("resume")
                        
                        flag = 1
                    
                        #start_time = time.time()
                        past_state = None
                        #time.sleep(0.5)
                        button_text = 'STOP'
    
    
    
    
    if start == True and current_state == "forward" and current_state != past_state:
        forward_start = time.time()
        clockwise(pA, full_dc, AIN1, AIN2,queue_A,time_A)
        clockwise(pB, full_dc, BIN1, BIN2,queue_B,time_B)
        past_state = "forward"
        

        
    if start == True and current_state == "stop" and current_state != past_state:
        stop(pA, queue_A, time_A)
        stop(pB, queue_B, time_B)
        past_state = "stop"
        
    if start == True and current_state == "backward" and current_state != past_state:
        counterclockwise(pA, full_dc, AIN1, AIN2, queue_A,time_A)
        counterclockwise(pB, full_dc, BIN1, BIN2, queue_B,time_B)
        past_state = "backward"
    if start == True and current_state == "left" and current_state != past_state:
        clockwise(pA, half_dc, AIN1, AIN2,queue_A,time_A)
        clockwise(pB, full_dc, BIN1, BIN2,queue_B,time_B)
        past_state = "left"
    if start == True and current_state == "right" and current_state != past_state:
        clockwise(pA, full_dc, AIN1, AIN2,queue_A,time_A)
        clockwise(pB, half_dc, BIN1, BIN2,queue_B,time_B)        
        past_state = "right"
    if flag == 1 and start == True and (time.time() - start_time)%24 > 0 and (time.time() - start_time)%24 < 3:
        current_state = "forward"
        
    if flag == 1 and start == True and (time.time() - start_time)%24 > 3 and (time.time() - start_time)%24 < 6:
        current_state = "stop"
        
    if flag == 1 and start == True and (time.time() - start_time)%24 > 6 and (time.time() - start_time)%24 < 9:
        current_state = "backward"
        
    if flag == 1 and start == True and (time.time() - start_time)%24 > 9 and (time.time() - start_time)%24 < 12:
        current_state = "stop"
        
    if flag == 1 and start == True and (time.time() - start_time)%24 > 12 and (time.time() - start_time)%24 < 15:
        current_state = "left"
        
    if flag == 1 and start == True and (time.time() - start_time)%24 > 15 and (time.time() - start_time)%24 < 18:
        current_state = "stop"
    
    if flag == 1 and start == True and (time.time() - start_time)%24 > 18 and (time.time() - start_time)%24 < 21:
        current_state = "right"    
        
    if flag == 1 and start == True and (time.time() - start_time)%24 > 21 and (time.time() - start_time)%24 < 24:
        current_state = "stop"
        
    
    pygame.display.flip()
    
    
    if not GPIO.input(27):
        code_run = False
        
    if time.time()-time_start>60:
        code_run = True
        



pA.stop()
pB.stop()

GPIO.output(AIN2, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(BIN2, GPIO.LOW)
GPIO.output(BIN1, GPIO.LOW)

GPIO.cleanup()

pygame.quit()
