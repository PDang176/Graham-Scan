# Pygame Constants
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

# Graham Scan Variables
points = []
anchor = None
hull = []