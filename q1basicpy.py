import pygame,sys
from numpy import random

def rect(x,y,w,h,color):
     rectangle = pygame.Surface((w, h))
     rectangle.fill(color)
     screen.blit(rectangle, (x,y))

pygame.init()
size=width,height=1000,800
screen=pygame.display.set_mode(size)
running=True
i=0
x,y=0,0
a,b=30,30
arr=[[0,0]]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
           running= False
    while (x>0 and x<1000) and (y>0 and y <1000):
      if i%2==0:
        k=random.choice([1,2,3,4,5,-1,-2,-3,-4,-5])
        if k>0:
            
            for m in range(1,k+1):
                x+=a*m
                arr.append([x,y])

            





