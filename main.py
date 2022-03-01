import pygame
import numpy as np

# Screen Constants
WIDTH = 800
HEIGHT = 800
RADIUS = 5
SPEED = 5 # FPS

#Color Constants
BLACK = (0, 0, 0) # Background
RED = (255, 0, 0) # In Hull / Connection
BLUE = (0, 0, 255) # Not in Hull
YELLOW = (255, 255, 0) # Testing for Hull / Testing Connection
GREEN = (0, 255, 0) # Fully Complete Convex Hull

def main():
    global screen, clock
    
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Graham Scan Algorithm")

    screen.fill(BLACK)

    


if __name__ == "__main__":
    main()