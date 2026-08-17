import pygame,sys
from numpy import random
def rect(x,y,w,h,color):
     rectangle = pygame.Surface((w, h))
     # Fill the surface with a color (e.g., red)
     rectangle.fill(color)

# Blit (draw) the surface onto the screen
     screen.blit(rectangle, (x,y))

pygame.init()

size=(1000,500)
screen=pygame.display.set_mode(size)
running=True
v=0
path=[]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            running= False
    screen.fill((0,0,0))
    #for x in range(-10,10):
      #  rect(500+30*x,250,30,30,(255,0,0))
    x,y=30,30 
    j=5   
    arr=[[]]
    if v==0:
         while x!=960: 
          i=random.choice([1,2,3,0])
          if x<30 and (y>30 and y<470):
               i=random.choice([1,2,3])
          elif x>970 and (y>30 and y<470):
               i=random.choice([1,0,3])
          elif y>470 and (x>30 and x<970):
               i=random.choice([1,0,2])
          elif y>30 and (x>30 and x<970):
               i=random.choice([3,0,2])
          elif x<30 and y<30:
               i=random.choice([2,3])
          elif x<30 and y>470:
               i=random.choice([2,1])
          elif x>970 and y<30:
               i=random.choice([0,3])
          elif x>970 and y>470:
               i=random.choice([0,1])
          else: i= random.choice([1,2,3,0]) 

          # 1,2,3,0 are respectively for up ,right,down,left
          if j!=i or j>5:
           if i==1:
               y-=30
           elif i==2:
               x=x+30
           elif i==3:
               y+=30
           else:
               x-=30
          j=(i+2)%4
          if [x,y] not in path:
            path.append([x,y])
             
    v=1
    for i in  path:
         rect(i[0],i[1],30,30,(0,0,255))   
    pygame.display.flip()
sys.exit()
#def neighbour():
    





