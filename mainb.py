import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import time
from random import randint
from math import atan2
from functools import cmp_to_key

# Create Points Variables (n points ranging from min to max)
n = 100
min = 0
max = 10000

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
#   a: Given Point
# Returns:
#   Polar angle between anchor and a
def polar_angle(a):
    global anchor
    x = a[0] - anchor[0]
    y = a[1] - anchor[1]
    return atan2(y, x)

# Calculates the cotangent formed between the anchor and the point
# Parameters:
#   a: Given Point
# Returns:
#   Cotangent between anchor and a
def cotan(a):
    global anchor
    x = a[0] - anchor[0]
    y = a[1] - anchor[1]
    if y == 0:
        return -max
    return -x / y

def compare(a, b):
    global anchor
    cross = ccw(anchor, a, b)
    if cross < 0:
        return -1
    if cross > 0:
        return 1
    return 0


# Calculates the squared distance between the anchor and the point
# Parameters:
#   a: Given Points
# Returns:
#   Squared distance between anchor and a
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
    # Calculate the cotangent of a random point in our array to use as our pivot
    pivot = cotan(arr[randint(0, len(arr) - 1)])
    for point in arr:
        angle = cotan(point)
        if angle < pivot:
            smaller.append(point)
        elif angle == pivot:
            equal.append(point)
        else:
            larger.append(point)
    return quicksort(smaller) + sorted(equal, key=distance) + quicksort(larger)

# Sort the passed in array by increasing polar angle from starting point
# Parameters:
#   arr: The array to sort
# Returns:
#   Recursive call to quicksort for smaller and larger
#   If equal return it sorted by distance
def quicksort2(arr):
    if len(arr) <= 1:
        return arr
    # Create 3 separate arrays according to if their polar angle are smaller, equal to, or larger than the pivot
    smaller = []
    equal = []
    larger = []
    # Calculate the cotangent of a random point in our array to use as our pivot
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

# Sort the passed in array by increasing polar angle from starting point
# Parameters:
#   arr: The array to sort
# Returns:
#   Recursive call to quicksort for smaller and larger
#   If equal return it sorted by distance
def quicksort3(arr):
    if len(arr) <= 1:
        return arr
    # Create 3 separate arrays according to if their polar angle are smaller, equal to, or larger than the pivot
    smaller = []
    equal = []
    larger = []
    # Calculate the cotangent of a random point in our array to use as our pivot
    pivot = arr[randint(0, len(arr) - 1)]
    for point in arr:
        comp = compare(point, pivot)
        if comp < 0:
            smaller.append(point)
        elif comp == 0:
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
def graham_scan(points, opoints=None, plot=False):
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
        plot_points(opoints, hull)

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

    # bottom, right, top, left
    polygon = [points[0] for _ in range(4)]

    for (x, y) in points[1:]:
        # Lowest y
        if y < polygon[0][1]:
            polygon[0] = [x, y]
        # Highest x
        if x > polygon[1][0]:
            polygon[1] = [x, y]
        # Highest y
        if y > polygon[2][1]:
            polygon[2] = [x, y]
        # Lowest x
        if x < polygon[3][0]:
            polygon[3] = [x, y]

    # Append polygon points to new points array without duplicates
    npoints = [polygon[0]]
    curr = polygon[0]
    for p in polygon[1:]:
        if p != curr:
            npoints.append(p)
            curr = p

    if len(npoints) < 3: # Not a polygon
        return points

    for i in range(len(npoints) - 1):
        x = [npoints[i][0], npoints[i + 1][0]]
        y = [npoints[i][1], npoints[i + 1][1]]
        plt.plot(x, y, color='yellow')
    plt.plot([npoints[0][0], npoints[-1][0]], [npoints[0][1], npoints[-1][1]], color='yellow')

    # Append points outside of polygon to new points array
    for p in points:
        # Check if point is inside of the polygon
        if is_inside_polygon(polygon, p):
            continue

        # Point is outside of the polygon so append
        npoints.append(p)
    
    return npoints

# Akl_Toussaint Heuristic to reduce the number of points needed for the Graham Scan
# Creates a octagon out of the bottom/right/top/left most points and 
# points with highest x/y sums and differences in the points array
# Currently doesn't account for the edge cases involving some points being the same
# Any point within this octagons will not appear in the final convex hull thus can be removed
# Parameters:
#   points: The points array to search through
# Returns:
#   npoints: The new points array with only possible points for the convex hull algorithm
def akl_toussaint_oct(points):
    # Lowest y, Highest difference, Highest x, Highest sum, Highest y, Lowest difference, Lowest x, Lowest sum
    polygon = [points[0] for _ in range(8)]

    for (x, y) in points[1:]:
        # Lowest y
        if y < polygon[0][1]:
            polygon[0] = [x, y]
        # Highest difference
        if x - y > polygon[1][0] - polygon[1][1]:
            polygon[1] = [x, y]
        # Highest x
        if x > polygon[2][0]:
            polygon[2] = [x, y]
        # Highest sum
        if x + y > polygon[3][0] + polygon[3][1]:
            polygon[3] = [x, y]
        # Highest y
        if y > polygon[4][1]:
            polygon[4] = [x, y]
        # Lowest difference
        if x - y < polygon[5][0] - polygon[5][1]:
            polygon[5] = [x, y]
        # Lowest x
        if x < polygon[6][0]:
            polygon[6] = [x, y]
        # Lowest sum
        if x + y < polygon[7][0] + polygon[7][1]:
            polygon[7] = [x, y]

    # Append polygon points to new points array without duplicates
    npoints = [polygon[0]]
    curr = polygon[0]
    for p in polygon[1:]:
        if p != curr:
            npoints.append(p)
            curr = p

    if len(npoints) < 3: # Not a polygon
        return points

    for i in range(len(npoints) - 1):
        x = [npoints[i][0], npoints[i + 1][0]]
        y = [npoints[i][1], npoints[i + 1][1]]
        plt.plot(x, y, color='yellow')
    plt.plot([npoints[0][0], npoints[-1][0]], [npoints[0][1], npoints[-1][1]], color='yellow')

    # Append points outside of polygon to new points array
    for p in points:
        # Check if point is inside of the polygon
        if is_inside_polygon(polygon, p):
            continue

        # Point is outside of the polygon so append
        npoints.append(p)
    
    return npoints

# Check if point is inside the polygon
# If the point is on the left of all line segments in the polygon then it's inside the polygon
# Parameters:
#   polygon: The points representing the polygon
#   p : The point we're checking 
# Returns:
#   True: p is inside the polygon
#   False: p is outside the polygon
def is_inside_polygon(polygon, p):
    # Length of the polygon
    n = len(polygon)

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # If p doesn't form a counter clockwise rotation with p1 and p2 then 
        # it's either on the polygon perimeter or outside the polygon
        if ccw(p1, p2, p) <= 0:
            return False
    
    return True

def main():
    global anchor

    # for i in range(10):
    # Create n random points
    points = [[randint(min, max), randint(min, max)] for _ in range(n)]

    # Get the starting time
    # start = time.time()

    # Run Akl-Toussaint Heuristic
    npoints = akl_toussaint_oct(points)
    anchor = npoints[0]

    # Find the anchor coordinate in the graph
    # anchor = get_anchor(points)

    # Sort points by increasing polar angle from anchor
    npoints = quicksort(npoints)

    # Call Graham Scan Algorithm
    graham_scan(npoints, points, True)

    # Get the ending time
    # end = time.time()

    # f = open("results/akl-toussaint107o.txt", "a")
    # f.write(str(end - start) + "\n")
    # f.close()

    # print()

if __name__ == "__main__":
    main()