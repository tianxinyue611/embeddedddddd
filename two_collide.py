import pygame
import sys
'''
import RPi.GPIO as GPIO
start_time = time.time()
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
'''

pygame.init()
clock = pygame.time.Clock()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
black = 0, 0, 0
code_run = True
ball1 = pygame.image.load("magic_ball.png")
ball1rect = ball1.get_rect()
speed1 = [1,1]

ball2 = pygame.image.load("ledlightblue.png")
ball2rect = ball2.get_rect(center=(200,100))
speed2 = [5,5]


while code_run:

    ball1rect = ball1rect.move(speed1)
    ball2rect = ball2rect.move(speed2)

    if ball1rect.left < 0 or ball1rect.right > width:
        speed1[0] = -speed1[0]
    if ball1rect.top < 0 or ball1rect.bottom > height:
        speed1[1] = -speed1[1]
    if ball2rect.left < 0 or ball2rect.right > width:
        speed2[0] = -speed2[0]
    if ball2rect.top < 0 or ball2rect.bottom > height:
        speed2[1] = -speed2[1]

    if ball1rect.colliderect(ball2rect):
        speed1[0] = -speed1[0]
        speed1[1] = -speed1[1]
        speed2[0] = -speed2[0]
        speed2[1] = -speed2[1]

    screen.fill(black)
    screen.blit(ball1, ball1rect)
    screen.blit(ball2,ball2rect)
    pygame.display.flip()

    '''
    if not GPIO.input(27):
        code_run = False

    now = time.time()
    elapsed = now - start_time
    if elapsed > 30:
        code_run = False
    '''

