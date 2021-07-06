import pygame
from pygame.locals import *

pygame.init()

width=600
height=650

#game vars
timer=pygame.time.Clock()
fps=60
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Flappy Bird')
floor_movement=0
floor_speed=5
over=False
flap=False


#bg image
back=pygame.image.load('media/background.png')
#fg image
fore=pygame.image.load('media/floor.png')

class Flappy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image_list=[]
        self.counter=0
        self.idx=0
        n=1
        while n<4:
            icon=pygame.image.load(f'media/flappy_{n}.png')
            self.image_list.append(icon)
            n+=1
        self.image=self.image_list[self.idx]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.velocity=0
        self.trigger=False

    def update(self):
        #downward motion
        if flap==True:
            if self.velocity<10:
                self.velocity+=0.75

            if self.rect.bottom<500:
                self.rect.y+=int(self.velocity)

        #upward motion
        if over==False:
            if pygame.mouse.get_pressed()[0]==1 and self.trigger==False:
                self.trigger=True
                self.velocity=-15

            if pygame.mouse.get_pressed()[0]==0:
                self.trigger=False

            #Animation
            self.counter=self.counter+1
            period=4

            if self.counter>period:
                self.idx+=1
                self.counter=0
                if(self.idx>=len(self.image_list)):
                    self.idx=0

            self.image=self.image_list[self.idx]

            #rotation
            self.image=pygame.transform.rotate(self.image_list[self.idx],self.velocity*(-1.5))
        else:
            self.image=pygame.transform.rotate(self.image_list[self.idx],-90)
            
bird_group=pygame.sprite.Group()
bird=Flappy(75,int(height/2)-50)
bird_group.add(bird)
#var
game=True

while game:
    #optimum 60 fps
    timer.tick(fps)
    #blit = Show image on screen
    screen.blit(back,(0,0))
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(fore,(floor_movement,500))

    if bird.rect.bottom>=500:
        flap=False
        over=True

    if over==False:
        floor_movement=floor_movement-floor_speed
        if abs(floor_movement)>30:
            floor_movement=0

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False
        if event.type==pygame.MOUSEBUTTONDOWN and over==False and flap==False:
            flap=True
    pygame.display.update()

pygame.quit()
