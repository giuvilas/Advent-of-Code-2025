#!/usr/bin/env python3

"""
Day 9: Movie Theater - Largest Rectangle Finder

Given a list of red tile coordinates on a grid, find the largest rectangle
that can be formed using any two red tiles as opposite corners.

The area of a rectangle with corners at (x1, y1) and (x2, y2) is:
    area = |x2 - x1| × |y2 - y1|
"""


def parse_tiles(filename):
    """
    Parse the input file to get a list of (x, y) coordinate tuples.
    Each line should be in the format: x,y
    """
    tiles = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(','))
            tiles.append((x, y))
    return tiles


def find_largest_rectangle(tiles):
    """
    Find the largest rectangle that can be formed using any two tiles
    as opposite corners.

    Algorithm:
    - For each pair of tiles (i, j), calculate the rectangle area
    - Area = |x2 - x1| × |y2 - y1|
    - Return the maximum area found

    Time complexity: O(n²) where n is the number of tiles
    Space complexity: O(1)
    """
    max_area = 0
    n = len(tiles)

    # Check all pairs of tiles
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            # Calculate the area of the rectangle
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            area = width * height

            # Update maximum area
            if area > max_area:
                max_area = area
                best_corners = ((x1, y1), (x2, y2))

    return max_area, best_corners


def main():
    # Parse the input file
    tiles = parse_tiles("input.txt")

    print(f"Number of red tiles: {len(tiles)}")

    # Find the largest rectangle
    max_area, corners = find_largest_rectangle(tiles)

    print(f"\nLargest rectangle area: {max_area}")
    print(f"Corners: {corners[0]} and {corners[1]}")
    print(f"\nAnswer: {max_area}")


if __name__ == "__main__":
    main()
