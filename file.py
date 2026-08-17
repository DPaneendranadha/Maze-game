import sys, pygame
pygame.init()

size = width, height = 1000, 500
speed = [1,1]
black = 255, 0, 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("example")
befor_scale=pygame.image.load("Nitro_Wallpaper_01.jpg")
ball = pygame.transform.scale(befor_scale,(100,100))
ballrect = ball.get_rect()

running =True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            running= False
           
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill((255,0,0))
    screen.blit(ball,ballrect)
   # font = pygame.font.Font(None, 36)  # None specifies default font, 36 is the font size

    #text = font.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
    #textpos = text.get_rect(centerx=width / 2, y=10)
    #screen.blit(text, t    extpos)
    
    pygame.display.flip()
sys.exit()