import pygame,sys
from numpy import random

##################### function to draw rectangles onto the surface of the maze ###########
def rect(x,y,w,h,color):
     #rectangle = pygame.Surface((w, h))
    # rectangle.fill(color)
     #screen.blit(rectangle, (x,y))
     pygame.draw.rect(maze_surface,color,(x,y,w,h))

##################### To define points for path ######################################
def path(s,e,vertices):
         if e-s>200:
           xaxis=[a for a in range(s,e) if a%40==0]
           x=random.choice(xaxis) 
           y=random.choice(yaxis) 
           vertices.append([x,y])
           path(s,x,vertices)
           path(x,e,vertices)
 ######################## one of the solution path ######################################          
def draw(x,y,x1,y1):
############################## 40 is the dimension of the block
      while x<x1:
       x+=40
       trail.append([x,y]) 
      if y<y1:
       while y<y1:
        y+=40
        trail.append([x,y])       
      elif y>y1:
       while y>y1:
        y-=40
        trail.append([x,y])  
pygame.init()
####################### Dimensions of the screen be 1000x1000 and game be 1000X800 #####################
size=width,height=1000,1000
screen=pygame.display.set_mode(size)
maze_surface=pygame.Surface((1000,800))
running=True
v=0
arr=[[]]
#dimension of the player should be (40,40) 
befor_scale=pygame.image.load("Nitro_Wallpaper_01.jpg")
ball = pygame.transform.scale(befor_scale,(40,40))
ballrect = ball.get_rect()
ballrect.x=0
ballrect.y=200
maze=[]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
           running= False

    if v!=1:
     yaxis=[x for x in range(200,height) if x%40==0]
     points=[] 
     trail=[]
     path(0,1000,points)
     a,b=0,200
     points.sort()
     print(points)
     for x in points:
       draw(a,b,x[0],x[1])
       a,b=x[0],x[1]
#vertices also gets included in the trail
     trail.append([0,200])
     trail.sort()
     #print()
     for x in range(0,1000,40):
        for y in range(200,1000,40):       
            if random.random() <0.5 and [x,y] not in trail:
                 maze.append([x,y])
    v=1 
    for x in range(0,1000,40):
        for y in range(200,1000,40):       
            if [x,y] in maze:
               rect(x,y,40,40,(255,0,0))
            else:rect(x,y,40,40,(255,255,255))
            rect(trail[-1][0],trail[-1][1],40,40,(0,150,0))
            rect(trail[0][0],trail[0][1],40,40,(0,0,200))
    # a and b are the current position of the players
    a=ballrect.x
    b=ballrect.y
    screen.blit(ball,ballrect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not prev_key_up:
      if [a,b-40] not in maze and b-40>=200:
        ballrect=ballrect.move(0,-40)
    prev_key_up=keys[pygame.K_UP] 
    if keys[pygame.K_DOWN] and not prev_key_down:
             if [a,b+40] not in maze and b+40<1000: 
                ballrect=ballrect.move(0,40)
    prev_key_down=keys[pygame.K_DOWN]
    if keys[pygame.K_RIGHT] and not prev_key_right:
       if [a+40,b] not in maze and a+40<1000: 
        ballrect=ballrect.move(40,0)
    prev_key_right=keys[pygame.K_RIGHT]
    if keys[pygame.K_LEFT] and not prev_key_left:
        if [a-40,b] not in maze and a-40>=0:
         ballrect=ballrect.move(-40,0)
    prev_key_left=keys[pygame.K_LEFT] 
    
    pygame.display.flip()
sys.exit()