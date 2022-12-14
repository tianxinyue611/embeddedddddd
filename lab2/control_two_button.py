import os
import pygame
from pygame.locals import *
import time
import RPi.GPIO as GPIO

# Initialize variables
starttime = time.time()
code_running = True
game_running = False
paused = False
framerate = 40 #framerate value for fast/slow buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
clock = pygame.time.Clock()

# Display on TFT, use touchscreen
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

# Initialize display constants
pygame.init()
pygame.mouse.set_visible(False)
WHITE = 255,255,255
BLACK = 0,0,0
size = width, height = 320,240
speed = [5,5]
speed2 = [7,7]
screen = pygame.display.set_mode((320,240))
ball = pygame.image.load('magic_ball.png')
ball2 = pygame.image.load('ledlightblue.png')
ball_rect = ball.get_rect(center=(50,50))
ball2_rect = ball2.get_rect(center=(100,100))

my_font = pygame.font.Font(None,30)
my_buttons = {'start':(40,180),'quit':(280,180)}
game_buttons = {'pause':(40,180),'fast':(130,180),'slow':(210,180), \
    'back':(280,180)}
screen.fill(BLACK)
hit_text = ""

# Continue looping until quit button or timeout
while code_running:
    clock.tick(framerate)
    screen.fill(BLACK)
    # balls are displayed and not paused - need to update location and speed
if (game_running):
    if(not paused):
           speed = [5,5]
speed2 = [7,7]
          ball_rect = ball_rect.move(speed)
          ball2_rect = ball2_rect.move(speed2)
          if ball_rect.left < 0 or ball_rect.right > width:
              speed[0] = -speed[0]
          if ball_rect.top < 0 or ball_rect.bottom > height:
              speed[1] = -speed[1]
          if ball2_rect.left < 0 or ball2_rect.right > width:
              speed2[0] = -speed2[0]
          if ball2_rect.top < 0 or ball2_rect.bottom > height:
              speed2[1] = -speed2[1]
          # check if balls collide with each other
          if ball_rect.colliderect(ball2_rect):
              speed[0] = -speed[0]
              speed[1] = -speed[1]
              speed2[0] = -speed2[0]
              speed2[1] = -speed[1]
        if(paused):
               speed11[0]=speed[0]
               speed[0]=0
               speed11[1]= speed[1]
               speed[1]=0
speed21[0]=speed2[0]
               speed2[0]=0
               speed21[1]= speed2[1]
               speed2[1]=0

    # ensures buttons will be displayed/checked whether game is paused/unpaused
    if (game_running):
        # pause,fast,slow,and back buttons displayed
        for my_text, text_pos in game_buttons.items():
            text_surface = my_font.render(my_text,True,WHITE)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        # balls displayed (in new location if unpaused)
        screen.blit(ball,ball_rect)
        screen.blit(ball2,ball2_rect)
        pygame.display.flip()
        # Check for button presses
        for event in pygame.event.get():
            if (event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            elif (event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y > 160:
                    if x < 60:
                        print 'pause pressed'
                        paused = not paused
                    elif x > 110 and x < 150:
                        print 'fast pressed'
                        framerate = framerate*1.1
                    elif x > 190 and x < 230:
                        print 'slow pressed'
                        framerate = framerate/0.8
                    elif x > 260:
                        print 'back pressed'
                        game_running = False
                        code_running = True
                        paused = False
    # Balls not displayed - start menu
    else:
        # start, quit buttons displayed
        for my_text, text_pos in my_buttons.items():
            text_surface = my_font.render(my_text,True,WHITE)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        # Display "hit"
        if (hit_text != ""):
            text_surface = my_font.render(hit_text,True,WHITE)
            rect = text_surface.get_rect(center=(100,100))
            screen.blit(text_surface,rect)
    # Check start screen button presses
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif (event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            if y > 160:
                if x < 60:
                    print 'start pressed'
                    game_running = True
                    code_running = True
                elif x > 260:
                    print 'quit pressed'
                    game_running = False
                    code_running = False
            else:
                hit_text="Hit at " + str(pos[0]) + "," + str(pos[1])
                print hit_text
    pygame.display.flip()
    # Check quit conditions
    if not GPIO.input(27):
        code_running = False
    now = time.time()
    elapsed = now - starttime
    if elapsed >= 30:
        code_running = False
