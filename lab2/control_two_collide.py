import pygame
import os
from pygame.locals import *
import time
import RPi.GPIO as GPIO



def two_collide():
    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    code_run = True

    my_buttons = {'Pause': (40, 200), 'Fast': (80, 200),'Slow':(120,200),'Back':(160,200)}
    my_button_rect = {}

    ball1 = pygame.image.load("xmas_ball.png")
    ball1rect = ball1.get_rect(center=(50, 50))
    ball1rect = ball1rect.inflate(-11, -11)
    speed1 = [1, 1]

    ball2 = pygame.image.load("ledlightblue.png")
    ball2rect = ball2.get_rect(center=(200, 100))
    ball2rect = ball2rect.inflate(-5, -5)
    speed2 = [1, 2]

    while code_run:
        time.sleep(0.003)

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
        screen.blit(ball2, ball2rect)

        # screen.fill(BLACK)

        for my_text, text_pos in my_buttons.items():
            text_surface = my_font.render(my_text, True, WHITE)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
            my_button_rect[my_text] = rect

            if (event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            elif (event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()

                for (my_text, rect) in my_button_rect.items():
                    if (rect.collidepoint(pos)):
                        if (my_text == 'Pause'):
                            speed1 = [0, 0]
                            speed2 = [0, 0]
                        if (my_text == 'Fast'):
                            speed1 = 2*speed1
                            speed2 = 2*speed2
                        if(my_text=='Slow'):
                            speed1 = 0.5*speed1
                            speed2 = 0.5*speed2
                        if(my_text=='Back'):
                            code_run = False

        pygame.display.flip()

        if not GPIO.input(27):
            code_run = False

# end of function





os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start_time = time.time()
pygame.init()

# pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
screen = pygame.display.set_mode((320, 240))

my_font = pygame.font.Font(None, 50)
text_font = pygame.font.Font(None, 20)
my_buttons = {'start': (80, 200), 'quit': (240, 200)}
screen.fill(BLACK)

my_button_rect = {}
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text, True, WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
    my_button_rect[my_text] = rect

pygame.display.flip()

code_run = True

while code_run:
    screen.fill(BLACK)
    for my_text, text_pos in my_buttons.items():
        text_surface = my_font.render(my_text, True, WHITE)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
        my_button_rect[my_text] = rect

    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif (event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x, y = pos

            text_show = "Touch at " + str(x) + " " + str(y)
            text = text_font.render(text_show, True, WHITE)
            text_rect = text.get_rect(center=(160, 120))
            screen.blit(text, text_rect)
            pygame.display.flip()

            print("touch", pos)

            for (my_text, rect) in my_button_rect.items():
                if (rect.collidepoint(pos)):
                    if (my_text == 'quit'):
                        code_run = False
                    elif (my_text == 'start'):
                        two_collide()

    pos = pygame.mouse.get_pos()
    if pos == None:
        continue;

    else:
        pos = pos;

    if not GPIO.input(27):
        code_run = False

    if time.time() - start_time > 30:
        code_run = False

pygame.quit()
