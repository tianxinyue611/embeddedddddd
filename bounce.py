import pygame     # Import pygame graphics library
import os    # for OS calls
import time

'''
import RPi.GPIO as GPIO
start_time = time.time()
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
'''

code_run = True
pygame.init()

size = width, height = 320, 240
speed1 = [2,2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("magic_ball.png")
ballrect1 = ball1.get_rect()

while code_run:
    ballrect1 = ballrect1.move(speed1)

    if ballrect1.left < 0 or ballrect1.right > width:
        speed1[0] = -speed1[0]
    if ballrect1.top < 0 or ballrect1.bottom > height:
        speed1[1] = -speed1[1]

    screen.fill(black)               # Erase the Work space
    screen.blit(ball1, ballrect1)
    pygame.display.flip()        # display workspace on screen
    '''
    if not GPIO.input(27):
        code_run = False
        
    now = time.time()
    elapsed = now - start_time
    if elapsed > 30:
        code_run = False
    '''

pygame.quit()