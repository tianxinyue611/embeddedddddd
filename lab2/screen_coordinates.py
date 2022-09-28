import pygame
import os
from pygame.locals import *
import time
import RPi.GPIO as GPIO

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)

start_time = time.time()
pygame.init()

#pygame.mouse.set_visible(False)

WHITE = 255,255,255
BLACK = 0,0,0
screen = pygame.display.set_mode((320,240))

my_font = pygame.font.Font(None,50)
text_font = pygame.font.Font(None,20)
my_buttons = {'quit':(150,200)}
screen.fill(BLACK)

my_button_rect = {}
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text,True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
    my_button_rect[my_text] = rect

pygame.display.flip()

code_run = True

while code_run:
    screen.fill(BLACK)
    for my_text, text_pos in my_buttons.items():
        text_surface = my_font.render(my_text,True,WHITE)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
        my_button_rect[my_text] = rect
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
          
            text_show= "Touch at " + str(x)+ " "+str(y)
            text = text_font.render(text_show,True,WHITE)
            text_rect = text.get_rect(center=(160,120))
            screen.blit(text,text_rect)
            pygame.display.flip()
            
            print("touch", pos)


            for(my_text,rect) in my_button_rect.items():
                if(rect.collidepoint(pos)):
                    if(my_text == 'quit'):
                        code_run = False
                        
    pos = pygame.mouse.get_pos()                 
    if pos==None:
        continue;
    
    else:
        pos=pos;


    if not GPIO.input(27):
        code_run = False

    if time.time()-start_time>30:
        code_run = False
        


pygame.quit()
