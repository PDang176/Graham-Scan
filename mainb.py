import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import time
from random import randint
from math import atan2

# Create Points Variables (n points ranging from min to max)
n = 10000000
min = 0
max = 1000000000

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
# Parameters:
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

# Plot the passed in points array and hull using matplotlib
# Parameters:
#   points: The points array to plot
#   hull: The convex hull to plot (Default: None)
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

# Find the convex hull of the given points array
# Parameters:
#   points: The array to loop through
def graham_scan(points, plot=False):
    global anchor

    # Initialize hull to anchor and the first point (not including anchor) in points
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

    if plot:
        plot_points(points, hull)

# Akl_Toussaint Heuristic to reduce the number of points needed for the Graham Scan
# Creates a quadrilateral out of the left/right/top/bottom most points in the points array
# Currently doesn't account for the edge cases involving some points being the same
# Any point within this quadrilateral will not appear in the final convex hull thus can be removed
# Parameters:
#   points: The points array to search through
# Returns:
#   npoints: The new points array with only possible points for the convex hull algorithm
def akl_toussaint(points):
    # New points array to return after heuristic is completed
    npoints = []

    # left, right, bottom, top
    polygon = [points[0] for _ in range(4)]

    # Create polygon
    for p in points[1:]:
        if p[0] < polygon[0][0]:
            polygon[0] = p
        elif p[0] > polygon[1][0]:
            polygon[1] = p
        if p[1] < polygon[2][1]:
            polygon[2] = p
        elif p[1] > polygon[3][1]:
            polygon[3] = p

    # Append polygon points to new points array
    npoints.append(polygon[0])
    npoints.append(polygon[1])
    if polygon[2] != polygon[0] and polygon[2] != polygon[1]:
        npoints.append(polygon[2])
    if polygon[3] != polygon[0] and polygon[3] != polygon[1]:
        npoints.append(polygon[3])

    if len(npoints) == 2:
        return points
    
    # Append points outside of polygon to new points array
    for p in points:
        # Check if point is one of the polygon points
        if p == polygon[0] or p == polygon[1] or p == polygon[2] or p == polygon[3]:
            continue

        # Check if point is inside of the polygon
        if is_inside_polygon(polygon, p):
            continue

        # Point is outside of the polygon so append
        npoints.append(p)
    
    return npoints

# Use barycentric coordinate system to determine if point is inside the polygon
# Information taken from cs130 class
# https://www.cs.ucr.edu/~craigs/courses/2020-winter-cs-230/lectures/barycentric-coordinates.pdf
# Forms 2 triangles within the polygon if passed 4 coordinates and checks if the point is within one of the 2 triangles
# Parameters:
#   polygon: The coordinates representing the polygon
#   p : The point to check if it's inside the polygon
# Returns:
#   True: p is inside the polygon
#   False: p is outside the polygon
def is_inside_polygon(polygon, p):
    # Create a triangle using 3 coordinates of polygon
    ABC = area(polygon[0], polygon[1], polygon[2])
    alpha = area(p, polygon[1], polygon[2]) / ABC
    beta = area(p, polygon[2], polygon[0]) / ABC
    gamma = area(p, polygon[0], polygon[1]) / ABC

    # Check if inside triangle made by 3 coordinates of polygon
    if alpha >= 0 and beta >= 0 and gamma >= 0:
        return True
    
    # Polygon is only 3 coordinates
    if len(polygon) == 3:
        return False
    
    # Create a triangle representing the other half of the polygon
    ABC = area(polygon[0], polygon[1], polygon[3])
    alpha = area(p, polygon[1], polygon[3]) / ABC
    beta = area(p, polygon[3], polygon[0]) / ABC
    gamma = area(p, polygon[0], polygon[1]) / ABC

    # Check if inside triangle made by 3 coordinates of polygon
    return alpha >= 0 and beta >= 0 and gamma >= 0

# Area of triangle given by vertices a, b, and c
# Parameters:
#   a, b, c: Vertices of the triangle
def area(a, b, c):
    return 0.5 * (((b[0] * c[1]) - (c[0] * b[1])) + ((c[0] * a[1]) - (a[0] * c[1])) + ((a[0] * b[1]) - (b[0] * a[1])))

def main():
    global anchor

    for i in range(10):
        # Create n random points
        points = [[randint(min, max), randint(min, max)] for _ in range(n)]

        # Get the starting time
        start = time.time()

        # # Original
        # npoints = points

        # Run Akl-Toussaint Heuristic
        npoints = akl_toussaint(points)

        # Find the anchor coordinate in the graph
        anchor = get_anchor(npoints)

        # Sort points by increasing polar angle from anchor
        npoints = quicksort(npoints)
        
        # Call Graham Scan Algorithm
        graham_scan(npoints)

        # Get the ending time
        end = time.time()

        f = open("results/akl-toussaint107b.txt", "a")
        f.write(str(end - start) + "\n")
        f.close()


if __name__ == "__main__":
    main()