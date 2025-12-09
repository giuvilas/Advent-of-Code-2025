#!/usr/bin/env python3

"""
Day 9 Part 2: Movie Theater - Rectangle with Polygon Constraint

The red tiles form a closed polygon (connected in list order).
Green tiles are:
  1. On the edges connecting consecutive red tiles
  2. Inside the polygon

A valid rectangle must:
  - Have red tiles at opposite corners
  - Only contain red or green tiles (must be entirely within the polygon)
"""


def parse_tiles(filename):
    """Parse the input file to get a list of (x, y) coordinate tuples."""
    tiles = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(','))
            tiles.append((x, y))
    return tiles


def point_in_polygon(x, y, polygon):
    """
    Check if point (x, y) is inside or on the boundary of the polygon.
    Uses the ray casting algorithm.

    polygon: list of (x, y) tuples forming a closed polygon
    """
    n = len(polygon)
    inside = False

    x1, y1 = polygon[0]
    for i in range(1, n + 1):
        x2, y2 = polygon[i % n]

        # Check if point is on the edge
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            # Check if point is collinear with edge
            cross = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
            if cross == 0:
                return True  # On the boundary

        # Ray casting algorithm
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x1 == x2 or x <= xinters:
                        inside = not inside

        x1, y1 = x2, y2

    return inside


def is_rectangle_valid(x1, y1, x2, y2, polygon):
    """
    Check if a rectangle with corners at (x1,y1) and (x2,y2) is entirely
    within the polygon.

    We check:
    1. All four corners are inside or on the polygon
    2. Sample points along the edges to ensure no parts extend outside
    """
    # Normalize so x1 <= x2 and y1 <= y2
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    # Check all four corners
    corners = [
        (x1, y1), (x1, y2),
        (x2, y1), (x2, y2)
    ]

    for x, y in corners:
        if not point_in_polygon(x, y, polygon):
            return False

    # Sample points along edges more densely
    # For large rectangles, sample every ~500 cells to catch concave regions
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    # Sample horizontal edges (top and bottom)
    step_x = max(1, width // 200)  # Sample ~200 points across width
    for x in range(x1, x2 + 1, step_x):
        if not point_in_polygon(x, y1, polygon):
            return False
        if not point_in_polygon(x, y2, polygon):
            return False

    # Sample vertical edges (left and right)
    step_y = max(1, height // 200)  # Sample ~200 points across height
    for y in range(y1, y2 + 1, step_y):
        if not point_in_polygon(x1, y, polygon):
            return False
        if not point_in_polygon(x2, y, polygon):
            return False

    # Sample interior points in a grid pattern
    step_x_interior = max(1, width // 20)
    step_y_interior = max(1, height // 20)
    for x in range(x1 + step_x_interior, x2, step_x_interior):
        for y in range(y1 + step_y_interior, y2, step_y_interior):
            if not point_in_polygon(x, y, polygon):
                return False

    return True


def find_largest_valid_rectangle(tiles):
    """
    Find the largest rectangle with red corners that is entirely within
    the polygon formed by the red tiles.
    """
    max_area = 0
    best_corners = None
    n = len(tiles)

    # The tiles form a polygon in the order they appear in the list
    polygon = tiles

    print(f"Checking {n * (n - 1) // 2} rectangle candidates...")

    checked = 0
    # Check all pairs of red tiles as potential corners
    for i in range(n):
        if i % 50 == 0:
            print(f"Progress: {i}/{n} tiles checked...")

        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            # Calculate area
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height

            # Only check if this could beat our current max
            if area <= max_area:
                continue

            # Check if rectangle is valid (entirely within polygon)
            if is_rectangle_valid(x1, y1, x2, y2, polygon):
                max_area = area
                best_corners = ((x1, y1), (x2, y2))
                print(f"  New max area: {max_area} at {best_corners}")

            checked += 1

    print(f"Checked {checked} candidate rectangles")
    return max_area, best_corners


def main():
    tiles = parse_tiles("input.txt")

    print(f"Number of red tiles (polygon vertices): {len(tiles)}")
    print()

    max_area, corners = find_largest_valid_rectangle(tiles)

    print(f"\n{'='*60}")
    print(f"Largest valid rectangle area: {max_area}")
    if corners:
        print(f"Corners: {corners[0]} and {corners[1]}")
    print(f"\nAnswer: {max_area}")


if __name__ == "__main__":
    main()
