import pygame     # Import pygame graphics library
import os    # for OS calls
'''
import RPi.GPIO as GPIO
start_time = time.time()
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb0')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
'''

code_run = True


pygame.init()

size = width, height = 320, 240
speed1 = [1,1]
speed2 = [5,5]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball1 = pygame.image.load("magic_ball.png")
ball2 = pygame.image.load("ledlightblue.png")
ballrect1 = ball1.get_rect()
ballrect2 = ball2.get_rect()

while 1:
    ballrect1 = ballrect1.move(speed1)
    ballrect2 = ballrect2.move(speed2)

    if ballrect1.left < 0 or ballrect1.right > width:
        speed1[0] = -speed1[0]
    if ballrect1.top < 0 or ballrect1.bottom > height:
        speed1[1] = -speed1[1]
    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]


    screen.fill(black)               # Erase the Work space
    screen.blit(ball1, ballrect1)
    screen.blit(ball2, ballrect2)
    pygame.display.flip()        # display workspace on screen

    '''
    if not GPIO.input(27):
        code_run = False

    now = time.time()
    elapsed = now - start_time
    if elapsed > 30:
        code_run = False
    '''