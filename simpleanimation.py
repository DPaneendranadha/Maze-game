import pygame
import sys
# Define the sprite images
pygame.init()
size = width,height = 900,860
screen = pygame.display.set_mode(size)
r1 = pygame.image.load("r1.png").convert()
r2 = pygame.image.load("r2.png").convert()
r3 = pygame.image.load("r3.png").convert()
r4 = pygame.image.load("r4.png").convert()
r5 = pygame.image.load("r5.png").convert()
r6 = pygame.image.load("r6.png").convert()
r7 = pygame.image.load("r7.png").convert()
r1_=pygame.transform.scale(r1,(100,100))
r2_=pygame.transform.scale(r2,(100,100))
r3_=pygame.transform.scale(r3,(100,100))
r4_=pygame.transform.scale(r4,(100,100))
r5_=pygame.transform.scale(r5,(100,100))
r6_=pygame.transform.scale(r6,(100,100))
r7_=pygame.transform.scale(r7,(100,100))
r1r=pygame.transform.rotate(r1_,90*2)
r2r=pygame.transform.rotate(r2_,90*2)
r3r=pygame.transform.rotate(r3_,90*2)
r4r=pygame.transform.rotate(r4_,90*2)
r5r=pygame.transform.rotate(r5_,90*2)
r6r=pygame.transform.rotate(r6_,90*2)
r7r=pygame.transform.rotate(r7_,90*2)
# Define the list of sprite images
sprite_images = [r1r, r2r, r3r, r4r, r5r, r6r, r7r]
running=True
clock = pygame.time.Clock()
# Define the variable to keep track of the current sprite image
sprite_index = 0
def update_sprite(x,y):
    # Increment the sprite index
    global sprite_index
    sprite_index += 1

    # Reset the sprite index if it is greater than the number of sprite images
    if sprite_index >= len(sprite_images):
        sprite_index = 0

    # Draw the current sprite image on the maze surface
    screen.blit(sprite_images[sprite_index], (x,y))
# Game loop
x,y=450,400
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((150,150,150))
    # Update the sprite image
    
    

    update_sprite(x,y)

    # Update the display
    pygame.display.flip()
    clock.tick(12)

# Quit Pygame
pygame.quit()
sys.exit()