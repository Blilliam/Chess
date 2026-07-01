import pygame
import sys
from Board import Board
from GameObject import GameObject
import Constants

# Initialize all imported pygame modules
pygame.init()


# Window setup
BASE_WIDTH, BASE_HEIGHT = 800, 600
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("My First Pygame")
gameObj = GameObject()

# Game clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Main Game Loop

while gameObj.isRunning:

    gameObj.handleEvent()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 3. Drawing/Rendering
    screen.fill((40, 44, 52))  # Clears screen with a dark gray color
    
    gameObj.draw(screen)
    

    # Update the full display Surface to the screen
    pygame.display.flip()

    # Limit the loop to 60 frames per second
    clock.tick(FPS)

# Clean exit
pygame.quit()
sys.exit()