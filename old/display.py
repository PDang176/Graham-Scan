import pygame
import graham_scan as gs
import vars

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

def run():
    global screen, clock, scale

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Graham Scan Algorithm")

    screen.fill(BLACK)

    scale = [WIDTH / vars.max, HEIGHT / vars.max]

    draw_graph()
    update()
    pygame.time.delay(2000) # Wait 2 seconds to load in screen before starting

    # Graham Scan Algorithm
    gs.set_anchor()

    # Loop through all remaining points
    for point in vars.points[1:]:
        while gs.ccw(vars.hull[-2], vars.hull[-1], point) <= 0:
            del vars.hull[-1]
            if len(vars.hull) < 2:
                break
        vars.hull.append(point)
        print(point)
        update()

    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def draw_graph():
    global screen, clock, scale
    for point in vars.points:
        p = [point[0]* scale[0], point[1] * scale[1]]
        pygame.draw.circle(screen, BLUE, p, RADIUS)
    
    for point in vars.hull:
        p = [point[0]* scale[0], point[1] * scale[1]]
        pygame.draw.circle(screen, RED, p, RADIUS)

def update():
    global clock
    draw_graph()
    pygame.display.update()
    clock.tick(SPEED)