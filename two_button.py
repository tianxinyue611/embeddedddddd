import pygame
import os
from pygame.locals import *

#os.putenv('SDL_VIDEODRIVER','fbcon')
#os.putenv('SDL_FBDEV','/dev/fb1')
#os.putenv('SDL_MOUSEDRV','TSLIB')
#os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

pygame.init()

pygame.mouse.set_visible(False)

WHITE = 255,255,255
BLACK = 0,0,0
screen = pygame.display.set_mode((320,240))

my_font = pygame.font.Font(None,50)
my_buttons = {'button1':(80,180),'button2':(240,180)}
screen.fill(BLACK)

my_button_rect = {}
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text,True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
    my_button_rect[my_text] = rect

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            #x,y = pos
            #if y > 120:
                #if x < 160:
                    #print("button1 pressed")
                #else:
                    #print("button2 pressed")
            for(my_text,rect) in my_button_rect.items():
                if(rect.collidepoint(pos)):
                    if(my_text == 'button1'):
                        print("button1 pressed")
                    if(my_text=='button2'):
                        print("button2 pressed")
