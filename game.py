import pygame
from pygame.locals import *

pygame.init()

width=700
height=750

#game vars
timer=pygame.time.Clock()
fps=60
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Flappy Bird')
floor_movement=0
floor_speed=4

#bg image
back=pygame.image.load('media/background.png')
#fg image
fore=pygame.image.load('media/floor.png')
game=True

while game:
    #optimum 60 fps
    timer.tick(fps)
    #blit = Show image on screen
    screen.blit(back,(0,0))
    screen.blit(fore,(floor_movement,500))
    floor_movement=floor_movement-floor_speed

    if abs(floor_movement)>30:
        floor_movement=0

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False

    pygame.display.update()

pygame.quit()
