import pygame
import sys
from numpy import random
from fun import *

pygame.init()
####################### Dimensions of the screen be 1500X900 and game be 1000X800 #####################
size = width,height = 900,860
screen = pygame.display.set_mode(size)
def image(image,surface,w,h,x,y):
   img=pygame.image.load(image).convert()
   img=pygame.transform.scale(img,(w,h))
   img_rect=img.get_rect()
   img_rect.x=x
   img_rect.y=y
   surface.blit(img,img_rect)

background_image = pygame.image.load("mainbg.jpg").convert()
ship = pygame.transform.scale(background_image,(1500,1000))
#############################   BUTTONS   ################################
start_button=pygame.image.load("start.png").convert()
start=pygame.transform.scale(start_button,(495*0.6,195*0.6))

start_rect=start.get_rect()
start_rect.center=width/2,height/2
new=pygame.image.load("home.jpeg").convert()
new_game=pygame.transform.scale(new,(210,50))
new_game.set_alpha(0)
new_rect=new_game.get_rect()
new_rect.x=345
new_rect.y=700

exit=pygame.image.load("exit.jpeg").convert()
exit_game=pygame.transform.scale(exit,(120,50))
exit_game.set_alpha(0)
exit_rect=exit_game.get_rect()
exit_rect.x=570
exit_rect.y=760
L1_button=pygame.image.load("start.png").convert()
L1=pygame.transform.scale(L1_button,(90,90))
L1.set_alpha(0)
L1_rect=L1.get_rect()
L1_rect.center=220,615
L2_button=pygame.image.load("start.png").convert()
L2=pygame.transform.scale(L2_button,(90,90))
L2.set_alpha(0)
L2_rect=L2.get_rect()
L2_rect.center=340,610
L3_button=pygame.image.load("start.png").convert()
L3=pygame.transform.scale(L3_button,(90,90))
L3.set_alpha(0)
L3_rect=L3.get_rect()
L3_rect.center=450,610


###### MAZE SURFACE ########
maze_surface=pygame.Surface((1600,1600))
logo=pygame.image.load("logo1.jpg").convert()
Title=pygame.transform.scale(logo,(678,233))
pygame.display.set_caption("HOME PAGE")
######################## DISPLAY SCREEN #####################
display=pygame.Rect(0,0,1600,800)
running=True
screen_var=0
v=0   # variable for initializing maze and to draw it once
#dimension of the player should be (40,40) 
befor_scale=pygame.image.load("try.png")

player = pygame.transform.scale(befor_scale,(50,50))
player_rect = player.get_rect()
############ Initial position of the ball should be at the top left corner of the maze########
maze=[]
clock = pygame.time.Clock()
################ Score , lives , points ################
score=0
gold_imag = pygame.image.load("gold.png").convert()
gold_image = pygame.transform.scale(gold_imag,(50,50))
island_img = pygame.image.load("grass.jpg").convert()
island = pygame.transform.scale(island_img,(80,80))
pause=False
################################################################3

def exit_fun():
  
    # Create a rectangle
    rect = pygame.Surface((200, 200))
    rect.fill((255, 255, 255))

    # Draw the rectangle on the maze surface
    maze_surface.blit(rect, (750-200,500-200))

    # Initialize the font object
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    # Create the text
    text = font.render("Do you really want to quit the game?", True, (0, 0, 0))

    # Draw the text on the rectangle
    rect.blit(text, (50, 50))

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check if the mouse is over the rectangle
    if rect.collidepoint(mouse_pos):
        # Draw the "Yes" and "No" buttons
        yes_button = font.render("Yes", True, (255, 0, 0))
        no_button = font.render("No", True, (255, 0, 0))
        rect.blit(yes_button, (50, 100))
        rect.blit(no_button, (150, 100))

        # Get the mouse click event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is over the "Yes" button
                if rect.collidepoint(event.pos, (50, 100, yes_button.get_width(), yes_button.get_height())):
                    # Exit the game
                    pygame.quit()
                    sys.exit()
                # Check if the mouse is over the "No" button
                elif rect.collidepoint(event.pos, (150, 100, no_button.get_width(), no_button.get_height())):
                    # Do nothing
                    pass
    else:
        # Do nothing
        pass
def pause_fun():
    pause=True
    pause_surf=pygame.Surface((200,200))
    pause_surf.fill((255,255,0))
    pause_rect=pause_surf.get_rect()
    maze_surface.blit(pause_surf,(550,300))
    for event in pygame.event.get() :
        if event.type==pygame.MOUSEBUTTONDOWN:
           if pause_rect.collidepoint(event.pos):
              screen_var=0
      
        
while running :
    key = pygame.key.get_pressed()
    for event in pygame.event.get() :
        if event.type==pygame.QUIT or key[pygame.K_ESCAPE]  :
            running= False
        elif event.type==pygame.MOUSEBUTTONDOWN:
             if new_rect.collidepoint(event.pos):
                screen_var=4
             elif exit_rect.collidepoint(event.pos):
                running=False
################ MAIN PAGE 1 ################
    if screen_var==0 :
        image("openingscreen.jpg",screen,width,height,0,0)
       # screen.blit(Title,(390,100))
       # screen.blit(start,start_rect)     
        screen.blit(new_game,new_rect)
        screen.blit(exit_game,exit_rect)
        
        pygame.font.quit()
        
          
        pygame.display.flip()
        keys=pygame.key.get_pressed()
    elif screen_var==4:
         image("nextscreen.jpg",screen,width,height,0,0)
         screen.blit(L1,L1_rect)
         screen.blit(L2,L2_rect)
         screen.blit(L3,L3_rect)
         for event in pygame.event.get():
          if event.type==pygame.MOUSEBUTTONDOWN:
           if L1_rect.collidepoint(event.pos):
              screen_var=1
              level=160
              wp=3000
              hp=1600
              dim=50
           elif L2_rect.collidepoint(event.pos):
              screen_var=1
              level=120
              wp=3000
              hp=1600
              dim=50
           elif L3_rect.collidepoint(event.pos):
              screen_var=1
              level=80
   
              wp=3000
              hp=1600
              dim=50
         pygame.display.flip()
      
        
##################### GAME PAGE ############################
    elif screen_var==1 :
      if not pause:
       
        if v!=1:
           Life_left=3
#height is kept constant because it is relative to the left corner of the maze not the screeen
           yaxis=[x for x in range(0,hp) if x%dim==0] 
           points=[] 
           trail=[]
           maze=[]
           other_points=[]
           coins=[]
           wrong_walls=[]
           path(0,wp,points,level,dim,yaxis)
           a,b=0,0
           points.sort()
           start_time=pygame.time.get_ticks()
           end_time=start_time+10000
           for x in points:
             draw(a,b,x[0],x[1],dim,trail)
             a,b=x[0],x[1]
           draw(points[-1][0],points[-1][1],wp-dim,hp-dim,dim,trail)

           trail.append([0,0])
           trail.sort()
           print("Length of solution :",len(trail))
           
           for x in range(0,wp,dim):
            for y in range(0,hp,dim):       
             if random.random() <0.5 and [x,y] not in trail:
                 maze.append([x,y])
           print(len(maze))
           for x in range(0,wp,dim):
            for y in range(0,hp,dim):       
             if [x,y] not in maze and [x,y] not in trail:
                 other_points.append([x,y])
      ######### Finish of the maze ##############
           i=0
           while i < 20:
              a = random.choice(range(len(other_points)))
              if [other_points[a][0],other_points[a][1]] not in coins:
                 coins.append([other_points[a][0],other_points[a][1]])
                 i+=1
           j=0
           while i < 20:
              a = random.choice(range(len(trail)))
              if [trail[a][0],trail[a][1]] not in coins:
                 coins.append([trail[a][0],trail[a][1]])
                 i+=1
           i=0
           while i < 40:
              a = random.choice(range(len(maze)))
              if [maze[a][0],maze[a][1]] not in wrong_walls:
                 wrong_walls.append([maze[a][0],maze[a][1]])
                 i+=1
           
              
              
           
        v=1 
        for x in range(0,wp,dim):
           for y in range(0,hp,dim):       
            if [x,y] in maze:
               wall=gold(x,y,dim,dim,"grass.jpg")
               wall.dra(maze_surface)
              
            else:
               
               rect(x,y,dim,dim,(0,0,255),maze_surface)
            rect(trail[-1][0],trail[-1][1],dim,dim,(0,150,0),maze_surface)
        for x in coins:
           money=gold(x[0],x[1],dim,dim,"gold.png")
           money.dra(maze_surface)
        for x in wrong_walls:
           w=WrongWall(x[0],x[1],dim,dim)
           w.draw(maze_surface)
        
            
################# To draw the maze  without player ################
        maze_surface.blit(player,player_rect)
        
        screen.blit(maze_surface,(0,40),display)
        a=player_rect.x
        b=player_rect.y
        if a>450 and a <=1300:
           display.x=a-450
        elif a<=450:
           display.x=0
        else:
           display.x=700
        if b>400 and b<=1200:
           display.y=b-400
        elif b<=400:
           display.y=0
        else:
           display.y=800
       



          
################ PLAYER UPDATE #########################
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not pause:
         if [a,b-dim] not in wrong_walls: 
          if  [a,b-dim] not in maze and b-dim>=0:
           player_rect=player_rect.move(0,-dim)
         else:
#$$$$$$$$$$$$$$$$$$$  we want to write a fun such that it would open a box saying that the player has lost a life and the score has been reduced by 10
             score-=10
             Life_left-=1
             player_rect.x=0
             player_rect.y=0          
        elif keys[pygame.K_DOWN] and not pause:
             if [a,b+dim] not in wrong_walls:
              if [a,b+dim] not in maze and b+dim<hp: 
                player_rect=player_rect.move(0,dim)
             else:
                score-=10
                Life_left-=1
                player_rect.x=0
                player_rect.y=0
                #sound               
        elif keys[pygame.K_RIGHT] and not pause :
           if [a+dim,b] not in wrong_walls:
            if [a+dim,b] not in maze and a+dim<wp: 
             player_rect=player_rect.move(dim,0)
           else:
               score-=10
               Life_left-=1
               player_rect.x=0
               player_rect.y=0
             
        elif keys[pygame.K_LEFT] and not pause:
          if [a-dim,b] not in wrong_walls:
           if [a-dim,b] not in maze and a-dim>=0:
             player_rect=player_rect.move(-dim,0)
          else:
              score-=10
              Life_left-=1
              player_rect.x=0
              player_rect.y=0
      
        if [a,b] in coins:
            coins.remove([a,b])
            score+=10
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        screen.fill((0, 0, 0), (1000, 10, 200, 50))
        current_time = pygame.time.get_ticks()
        remaining_time = 100000 - (current_time - start_time)
        current_time = pygame.time.get_ticks()
        remaining_time = 100000 - (current_time - start_time)
        text = font.render("Time: " + str(remaining_time / 1000), True, (255, 255, 255))
        screen.blit(text, (700, 40))
        pygame.font.quit()
      pygame.font.init()
      screen.fill((0, 0, 0), (10, 10, 200, 50))
      screen.fill((0, 0, 0), (800, 10, 200, 50))
       
        
######################## DISPLAY / STATUS BAR ############################
      font = pygame.font.Font(None, 36)
      text = font.render("Score: " + str(score), True, (255, 255, 255))
      screen.blit(text, (10, 10))
      text = font.render("LIFE LEFTS: " + str(Life_left), True, (255, 255, 255))
      screen.blit(text, (800, 10))
       



      pygame.font.quit()
        #######################################################################
  
        
        #to exit the game click escape and to end the game click space
      #new window open if the function  have some 
      # message fun():
      #    if messagebox(do you want to return )
      #    elif game over better luck next time ;
      # elif you found the one part of the one piece now next
      #  your score time taken and the number of coins collected
      #   no .of lifes left
      if keys[pygame.K_ESCAPE] and not prev :
            screen_var=0
            v=0
            player_rect.x=0
            player_rect.y=0
            maze=[]
            points=[]
            score=0
            coins=[]
            select=0
          #  while select==0:
          #    if exit_fun():
          #       select+=1
         # if select==1 :
         #    pygame.quit()
         #    sys.exit()
            
      prev=keys[pygame.K_ESCAPE]
      if ([a,b] == [trail[-1][0],trail[-1][1]] or Life_left==0 or remaining_time<0 or keys[pygame.K_RETURN]) and not previ:
             screen_var=2

             player_rect.x=0
             player_rect.y=0
             v=0
             maze=[]
             points=[]
             trail=[]
             score=0
             coins=[]
             #exit_fun()
      previ=keys[pygame.K_ESCAPE]
      pygame.display.flip()
     
    else :
        pygame.font.init()
       
        end=pygame.font.Font(None,80)
        restart=end.render("Restart",True,(255,0,0))
        restart.set_alpha(0)
        restart_rect=restart.get_rect()
        restart_rect.center=450,530
        home=end.render("Restart",True,(255,0,0))
        home.set_alpha(0)
        home_rect=home.get_rect()
        home_rect.center=450,600
        exit2=end.render("Restart",True,(255,0,0))
        exit2.set_alpha(0)
        exit2_rect=exit2.get_rect()
        exit2_rect.center=450,680
        
        screen.fill((255,255,255))
        image("gamescreen.png",screen,width,height,0,0)
        screen.blit(restart,restart_rect)
        screen.blit(home,home_rect)
        screen.blit(exit2,exit2_rect)
        pygame.font.quit()
        pygame.display.flip()
        keys=pygame.key.get_pressed()
        for event in pygame.event.get() :
         if event.type==pygame.MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
             screen_var=1
             player_rect.x=0
             player_rect.y=0
             v=0
             maze=[]
             points=[]
             trail=[]
             display.x=0
             display.y=0
            elif home_rect.collidepoint(event.pos):
             screen_var=0
             player_rect.x=0
             player_rect.y=0
             v=0
             maze=[]
             points=[]
             trail=[]
             display.x=0
             display.y=0
            elif exit2_rect.collidepoint(event.pos):
             
             running=False
             
             
               

       
             
        
    clock.tick(10)



pygame.quit()
sys.exit()










