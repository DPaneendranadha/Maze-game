import pygame
import sys
from numpy import random

# Define the rect function
def rect(x, y, w, h, color):
    rectangle = pygame.Surface((w, h))
    rectangle.fill(color)
    screen.blit(rectangle, (x, y))

pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
running = True
v = 0


#defining movement object 
befor_scale=pygame.image.load("Nitro_Wallpaper_01.jpg")
ball = pygame.transform.scale(befor_scale,(40,40))
ballrect = ball.get_rect()
maze=[]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    if v != 1:
        for x in range(0, 1000, 40):
            for y in range(0, 800, 40):
                if random.random() < 0.5:  # Adjust the threshold as needed
                     maze.append([x,y])     
    v = 1
    
    screen.fill((150, 75, 0))
    for a in maze:
        rect(a[0],a[1],40,40,(0,255,0))
    
  # to draw the moving object   
    screen.blit(ball,ballrect)
               


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not prev_key_up:
        ballrect=ballrect.move(0,-20)
    prev_key_up=keys[pygame.K_UP] 
    if keys[pygame.K_DOWN] and not prev_key_down:
        ballrect=ballrect.move(0,20)
    prev_key_down=keys[pygame.K_DOWN]
    if keys[pygame.K_RIGHT] and not prev_key_right:
        ballrect=ballrect.move(20,0)
    prev_key_right=keys[pygame.K_RIGHT]
    if keys[pygame.K_LEFT] and not prev_key_left:
        ballrect=ballrect.move(-20,0)
    prev_key_left=keys[pygame.K_LEFT]      

    pygame.display.flip()

sys.exit()
