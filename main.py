import pygame
import vars
import graham_scan

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

def main():
    prompt = "How many nodes would you like to spawn? "
    n = int(input(prompt))
    graham_scan.create_points(n)
    run(n)

if __name__ == "__main__":
    main()