import pygame
import sys
from numpy import random
pygame.init()
size = width,height = 1000,800
screen = pygame.display.set_mode(size)
#screen1 = pygame.display.set_mode((500,250))
pygame.display.set_caption("HOME PAGE")
running=True
screen_var=0

def rect(x,y,w,h,color):
     rectangle = pygame.Surface((w, h))
     rectangle.fill(color)
     screen.blit(rectangle, (x,y))
def path(s,e,vertices):
 # print("path called with s =", s, "and e =", e)
        if e-s>200:
           xaxis=[a for a in range(s,e) if a%40==0]
  # print(xaxis)
           x=random.choice(xaxis) 
           y=random.choice(yaxis)
   #print(x,y)
           vertices.append([x,y])
           path(s,x,vertices)
           path(x,e,vertices)
def draw(x,y,x1,y1):
              #40 is the dimension of the block
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
v=0
arr=[[]]
#dimension of the player should be (40,40) 
befor_scale=pygame.image.load("Nitro_Wallpaper_01.jpg")
ball = pygame.transform.scale(befor_scale,(40,40))
ballrect = ball.get_rect()
maze=[]

clock = pygame.time.Clock()
while running :
    for event in pygame.event.get() :
        if event.type==pygame.QUIT :
            running= False
    if screen_var==0 :
        pygame.font.init()
        heading=pygame.font.Font(None,50)
        Select_level=pygame.font.Font(None,25)
        other =pygame.font.Font(None,30)
        Head= heading.render("MAzE GaMe ", True , (0,0,255))
        select= Select_level.render("Select Level :",True , (0,0,255))
        L_1=Select_level.render("1",True , (0,0,255))
        L_2=Select_level.render("2",True , (0,0,255))
        L_3=Select_level.render("3",True , (0,0,255))
        screen.fill((0,0,0))
        screen.blit(Head,(width/2,height/4))
        screen.blit(select,(width/2,height/2))
        screen.blit(L_1,(5*width/12,height*3/4))
        screen.blit(L_2,(6*width/12,height*3/4))
        screen.blit(L_3,(7*width/12,height*3/4))
        pygame.font.quit()
        pygame.display.flip()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_1] and not prev_key_state :
            screen_var=1
        prev_key_state=keys[pygame.K_1]
    elif screen_var==1 :
       
        if v!=1:
           yaxis=[x for x in range(0,height) if x%40==0]
           points=[] 
           trail=[]
           maze=[]
           path(0,1000,points)
           a,b=0,0
           points.sort()
           print(points)
           for x in points:
             draw(a,b,x[0],x[1])
             a,b=x[0],x[1]
#vertices also gets included in the trail
           trail.append([0,0])
           trail.sort()
     #print()
           for x in range(0,1000,40):
            for y in range(0,800,40):       
             if random.random() <0.5 and [x,y] not in trail:
                 maze.append([x,y])
            #elif [x,y] in trail:
            #     rect(x,y,40,40,(0,0,150))
        v=1 
        for x in range(0,1000,40):
           for y in range(0,800,40):       
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
        if keys[pygame.K_UP] :
          if  [a,b-40] not in maze and b-40>=0:
           ballrect=ballrect.move(0,-40)
        if keys[pygame.K_DOWN] :
             if [a,b+40] not in maze and b+40<800: 
                ballrect=ballrect.move(0,40)
    
        if keys[pygame.K_RIGHT] :
           if [a+40,b] not in maze and a+40<1000: 
             ballrect=ballrect.move(40,0)
        
        if keys[pygame.K_LEFT]:
           if [a-40,b] not in maze and a-40>=0:
             ballrect=ballrect.move(-40,0)
    
        pygame.display.flip()
        #to exit the game click escape and to end the game click space
        if keys[pygame.K_ESCAPE] and not prev :
            screen_var=0
        prev=keys[pygame.K_ESCAPE]
        if [a,b] == [trail[-1][0],trail[-1][1]] :
             screen_var=2
             ballrect.x=0
             ballrect.y=0
             v=0
             
        previ=keys[pygame.K_ESCAPE]
     
    else :
        pygame.font.init()
        end=pygame.font.Font(None,100)
        restart=end.render("Restart",True,(255,0,0))
        width_restart,height_restart=restart.get_size()
        home=end.render("Home page",True,(255,0,0))
        width_home,height_home=home.get_size()
        exit=end.render("Exit",True,(255,0,0))
        width_exit,height_exit=exit.get_size()
        screen.fill((255,255,255))
        screen.blit(restart,((width-width_restart)/2,(height/2-height_restart)/2))
        screen.blit(home,((width-width_home)/2,(height-height_home)/2))
        screen.blit(exit,((width-width_exit)/2,(3*height/2-height_exit)/2))
        pygame.font.quit()
        pygame.display.flip()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]  :
            screen_var=0
        
    clock.tick(10)



pygame.quit()
sys.exit()




