import pygame
from graham_scan import vars

# Screen Constants
WIDTH = 1000
HEIGHT = 1000
RADIUS = 5
SPEED = 5 # FPS

#Color Constants
BLACK = (0, 0, 0) # Background
RED = (255, 0, 0) # In Hull / Connection
BLUE = (0, 0, 255) # Not in Hull
YELLOW = (255, 255, 0) # Testing for Hull / Testing Connection
GREEN = (0, 255, 0) # Fully Complete Convex Hull

def run(n=20):
    global screen, clock

    pygame.init()

    screen = pygame.display.set_mode((vars.WIDTH, vars.HEIGHT))
    clock = pygame.time.Clock()

    screen.fill(vars.BLACK)

    update()
    pygame.time.delay(2000) # Wait 2 seconds to load in screen before starting

def update():
    global clock
    pygame.display.update()
    clock.tick(vars.speed)