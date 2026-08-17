import pygame
from numpy import random
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h,img):
        '''
        For simple sprites and power waves  
        '''
        super().__init__()
        self.image=pygame.image.load(img).convert()
        self.wall=pygame.transform.scale(self.image,(w,h))
        self.rect=self.wall.get_rect()
        self.rect.x=x
        self.rect.y=y
    def store(self,direction):
       '''
        For storing the direction of wave used when updating
        this is added only for the wave
        '''
       self.movement=direction
  
  
    def dra(self,screen):
         ''' To blit the sprite on the screen'''
         screen.blit(self.wall,self.rect)
class animate(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,img_array):
        ''' For animated sprites
            And the img_array contains the sprites in facing the right side and
            the code will make the images for the other directions

        '''
        self.converted_img=[]
        self.rot_0=[]
        self.rot_1=[]
        self.rot_2=[]
        self.rot_3=[]
        self.rotated_img=[self.rot_0,self.rot_1,self.rot_2,self.rot_3]
     
        for img in img_array:
            image=pygame.image.load(img).convert()
            image=pygame.transform.scale(image,(w,h))
            self.rot_0.append(image)
        super().__init__()
        for img in self.rot_0:
            image=pygame.transform.rotate(img,90)
            self.rot_1.append(image)
            image=pygame.transform.flip(img, True, False)
            self.rot_2.append(image)
            image=pygame.transform.rotate(img,270)
            self.rot_3.append(image)        
        self.sprite=self.rot_0[0]
        self.rect=self.sprite.get_rect()
        self.rect.x=x
        self.rect.y=y        
        self.index=0

    def update(self,x,y,direct,given:bool,k=0):
       ''' To update the sprite in the given direction 
           and given is used whether it is static or not '''
       if given:
        self.sprite=self.rotated_img[direct][self.index]
        self.rect=self.sprite.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.index+=1
        if self.index>=len(self.rotated_img[direct]):
            if k==0:
             self.index=0
            else :
             self.index-=1
 
       else:
          self.index=0
          self.sprite=self.rotated_img[direct][self.index]
          self.rect=self.sprite.get_rect()
          self.rect.x=x
          self.rect.y=y
    def move(self,var,i):
       ''' To move the sprite in the given direction '''    # 0-right 1-up 2-left 3-down
       if i==1:
          self.rect.y-=var
       if i==3:
          self.rect.y+=var
       if i==2 :
          self.rect.x-=var
       if i==0:
          self.rect.x+=var
    def enemy_update(self,var:int,req_ele):
        ''' For randomly updating the enemy'''
        i=0
        j=0
        while i==0 and j<20:
           j+=1
           self.ds=random.choice([1,2,3,0])
           self.move(var,self.ds)
           if pygame.sprite.spritecollideany(self,req_ele):
              self.move(-var,self.ds)   
             # print("collided") 
           elif  self.rect.x>=0 and self.rect.x<=1550 and self.rect.y>=0 and self.rect.y<=1550:
              i=1
           
           self.update(self.rect.x,self.rect.y,self.ds,1)

              
    def store(self,direction):
       self.movement=direction
    def wave_update(self):
         ''' To move the wave until it collides with walls or enemies'''
         
         self.move(40,self.movement)
         self.update(self.rect.x,self.rect.y,self.movement,1,1)
    def dra(self,screen):
        screen.blit(self.sprite,self.rect)

        


        
