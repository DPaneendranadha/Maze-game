import pygame,sys


pygame.init()
def exit_fun(screen):
    rect=pygame.Surface((750-200,500-200))
    screen.blit(rect,(255,255,255)) 
    
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Do you really want to quit the game", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    for event in pygame.event.get() :
        if event.type==pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            

    
