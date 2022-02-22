from random import randint
from math import atan2
from re import A

# Creates a random set of points
# Parameters:
#   n: The number of points created (Default: 20)
#   min: The minimum value for the point's x and y coordinate
#   max: The maximum value for the point's x and y coordinate
# Returns:
#   An array of n random points with their coordinates ranging from min to max
def create_points(n=20, min=0, max=100):
    return [[randint(min, max), randint(min, max)] for _ in range(n)]

# Calculates the polar angle formed between 2 points
# Parameters:
# 
def polar_angle(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return atan2(y, x)

# Calculates the squared distance between the 2 points
# Parameters:
#   a, b: Given Points
# Returns:
#   Squared distance of points a and b
def distance(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return x**2 + y**2

# https://algs4.cs.princeton.edu/91primitives/
# Determines whether or not the passed in points form a counterclockwise angle
# Parameters:
#   a, b, c: Given Points
# Returns:
#   1:  If counterclockwise angle
#   0:  If collinear
#   -1: If clockwise angle
def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

# Sort the passed in array by increasing polar angle from starting point
# Paramters:
#   arr: The array to sort
# Returns:
#   Recursive call to quicksort for smaller and larger
#   If equal return it sorted by distance
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    # Create 3 separate arrays according to if their polar angle are smaller, equal to, or larger than the pivot
    smaller = []
    equal = []
    larger = []
    # Calculate the polar angle of a random point in our array to use as our pivot
    pivot = polar_angle(arr[randint(0, len(arr) - 1)])
    for point in arr:
        angle = polar_angle(point)
