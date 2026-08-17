import pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the 'a' key is pressed
    keys = pygame.key.get_pressed()
    # how to use key for one time press not for the entire set of frames
    if keys[pygame.K_a] and not prev_key_state:
        print("The 'a' key is pressed")
    prev_key_state=keys[pygame.K_a]    

pygame.quit()
'''

Pygame provides key constant values for various keys on the keyboard. While it's not practical to list every single key constant here, I can provide a list of some commonly used key constants. You can find the complete list of key constants in the Pygame documentation.

Here are some common key constants in Pygame:

pygame.K_BACKSPACE
pygame.K_TAB
pygame.K_RETURN
pygame.K_ESCAPE
pygame.K_SPACE
pygame.K_LEFT
pygame.K_RIGHT
pygame.K_UP
pygame.K_DOWN
pygame.K_LSHIFT
pygame.K_RSHIFT
pygame.K_LCTRL
pygame.K_RCTRL
pygame.K_LALT
pygame.K_RALT
pygame.K_LMETA (Left Windows key on Windows, Left Command key on macOS)
pygame.K_RMETA (Right Windows key on Windows, Right Command key on macOS)
pygame.K_F1 to pygame.K_F12
pygame.K_0 to pygame.K_9
pygame.K_a to pygame.K_z
pygame.K_KP0 to pygame.K_KP9 (Keypad keys)
'''


#Another way to use keys in a FASTER way 
# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))