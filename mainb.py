import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from random import randint
from math import atan2

# Create Points Variables (n points ranging from min to max)
n = 100000
min = 0
max = 100000000

# Get the anchor coordinate for the graph
# Parameters:
#   points: A list of all points in the graph
# Returns:
#   The lowest y-coordinate and x-coordinate point on the graph
def get_anchor(points):
    min_index = None
    for i, (x, y) in enumerate(points):
        if min_index == None or y < points[min_index][1]:
            min_index = i
        if y == points[min_index][1] and x < points[min_index][0]:
            min_index = i
    
    return points[min_index]

# Calculates the polar angle formed between 2 points
# Parameters:
#   a, b: Given Points
# Returns:
#   Polar angle between a and b
def polar_angle(a):
    global anchor
    x = a[0] - anchor[0]
    y = a[1] - anchor[1]
    return atan2(y, x)

# Calculates the squared distance between the 2 points
# Parameters:
#   a, b: Given Points
# Returns:
#   Squared distance between a and b
def distance(a):
    global anchor
    x = a[0] - anchor[0]
    y = a[1] - anchor[1]
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
        if angle < pivot:
            smaller.append(point)
        elif angle == pivot:
            equal.append(point)
        else:
            larger.append(point)
    return quicksort(smaller) + sorted(equal, key=distance) + quicksort(larger)

def plot_points(points, hull=None):
    df = pd.DataFrame(points, columns=['x', 'y'])
    plt.scatter(x=df['x'], y=df['y'], s=5)
    
    # A hull was passed in to graph
    if(hull != None):
        for i in range(len(hull) - 1):
            x = [hull[i][0], hull[i + 1][0]]
            y = [hull[i][1], hull[i + 1][1]]
            plt.plot(x, y, color='red')
        plt.plot([hull[0][0], hull[-1][0]], [hull[0][1], hull[-1][1]], color='red')
    plt.show()

def main():
    global anchor
    # Create n random points
    points = [[randint(min, max), randint(min, max)] for _ in range(n)]

    # Find the anchor coordinate in the graph
    anchor = get_anchor(points)

    # Sort points by increasing polar angle from anchor
    points = quicksort(points)
    
    # Initialize hull to anchor and the first point not including anchor
    hull = [anchor, points[1]]

    # Loop through all remaining points
    for point in points[2:]:
        # If the last 2 points of the hull and the new point isn't ccw then delete the last point in hull
        while ccw(hull[-2], hull[-1], point) <= 0:
            del hull[-1]
            if len(hull) < 2:
                break
        # Adding the new point to the hull will be ccw
        hull.append(point)

    plot_points(points, hull)

if __name__ == "__main__":
    main()