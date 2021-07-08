import pygame
from pygame.locals import *
import random

pygame.init()

width=600
height=650

#restart image
restart=pygame.image.load('media/button.png')

#game vars
timer=pygame.time.Clock()
fps=60
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Flappy Bird')

floor_movement=0
floor_speed=5
over=False
flap=False
gap=80
interval=1000 #Every 2 seconds
latestpipe=pygame.time.get_ticks()-interval
score=0
pipe_area=False

#Fonts and Colours
font=pygame.font.SysFont('Showcard Gothic', 50)
clr_white=(255,255,255)

def text_score(scr,font,colour,x,y):
    score_image=font.render(scr,True,colour)
    screen.blit(score_image,(x,y))

def reset():
    bird.rect.x=75
    bird.rect.y=int(height/2)-50
    global score
    score=0
    pipes_group.empty()

#bg image
back=pygame.image.load('media/background.png')
#fg image
fore=pygame.image.load('media/floor.png')

class Restart():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def appear(self):
        #Mouse position
        click=False
        mouse_position=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position) and pygame.mouse.get_pressed()[0]==1:
            click=True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return click

restart_button=Restart((int)(width/2)-50,(int)(height/2)-200,restart)

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




class Pipes(pygame.sprite.Sprite):
    def __init__(self,x,y,orientation):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('media/pipe.png')
        self.rect=self.image.get_rect()
        # Orientation 0 for Top, 1 for Bottom
        if orientation==1:
            self.rect.topleft=[x,y+int(gap/2)]
        else:
            self.image=pygame.transform.flip(self.image,False,True) #(2nd parameter-Horizontal flip, 3rd parameter-Vertical Flip)
            self.rect.bottomleft=[x,y-int(gap/2)]

    def update(self):
        self.rect.x=self.rect.x-floor_speed
        if self.rect.right<0:
            self.kill()

bird_group=pygame.sprite.Group()
bird=Flappy(75,int(height/2)-50)
bird_group.add(bird)

pipes_group=pygame.sprite.Group()

#var
game=True

while game:
    #optimum 60 fps
    timer.tick(fps)
    #blit = Show image on screen
    screen.blit(back,(0,0))
    bird_group.draw(screen)
    bird_group.update()
    pipes_group.draw(screen)

    screen.blit(fore,(floor_movement,500))

    #Scores
    if len(pipes_group)>0:
        if pipe_area==False and pipes_group.sprites()[0].rect.left<bird_group.sprites()[0].rect.left and pipes_group.sprites()[0].rect.right>bird_group.sprites()[0].rect.right:
            pipe_area=True
        if pipe_area==True and pipes_group.sprites()[0].rect.right<bird_group.sprites()[0].rect.left:
            pipe_area=False
            score=score+1


    #score appearence
    text_score(str(score),font,clr_white,int(width/2),30)



    #Collision
    if pygame.sprite.groupcollide(bird_group,pipes_group,False,False) or bird.rect.top<=0:
        over=True

    if bird.rect.bottom>=500:
        flap=False
        over=True

    if over==False and flap==True:

        current_time=pygame.time.get_ticks()
        if current_time-latestpipe>interval:
            randomgap=random.randint(-100,100)
            lowerpipe=Pipes(width,int(height/2)+randomgap,1)
            upperpipe=Pipes(width,int(height/2)+randomgap,0)
            pipes_group.add(lowerpipe)
            pipes_group.add(upperpipe)
            latestpipe=current_time

        floor_movement=floor_movement-floor_speed
        if abs(floor_movement)>30:
            floor_movement=0

        pipes_group.update()



    #Restart Button functionality
    if over==True and restart_button.appear()==True:
        over=False
        reset()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False
        if event.type==pygame.MOUSEBUTTONDOWN and over==False and flap==False:
            flap=True
    pygame.display.update()

pygame.quit()
