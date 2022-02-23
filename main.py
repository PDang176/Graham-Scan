import pygame
import graham_scan

WIDTH = 1000
HEIGHT = 1000
RADIUS = 5

def run(n=20):
    pygame.init()

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    display.fill((0, 0, 0))

    pygame.display.update()


def main():
    prompt = "How many nodes would you like to spawn? "
    n = int(input(prompt))
    graham_scan.create_points(n)

if __name__ == "__main__":
    main()