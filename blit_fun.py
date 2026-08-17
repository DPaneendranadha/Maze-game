import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blitting Part of a Surface Example")

# Create a source surface
source_surface = pygame.Surface((200, 200))
source_surface.fill((255, 0, 0))  # Fill with red color

# Create a rectangle to represent the area to blit from the source surface
source_rect = pygame.Rect(0, 50, 200, 100)  # (x, y, width, height)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Blit a part of the source surface onto the screen
    screen.blit(source_surface, (100, 0), source_rect)

    # Update the display
    pygame.display.flip()

# Cleanly exit Pygame
pygame.quit()
