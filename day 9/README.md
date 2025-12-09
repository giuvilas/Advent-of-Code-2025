# Advent of Code 2025 - Day 9: Movie Theater

Solution for [Advent of Code 2025 Day 9](https://adventofcode.com/2025/day/9)

## Files

- `day9_movie_theater.py` - Python script that solves the challenge
- `input.txt` - Puzzle input (496 red tile coordinates)
- `day9part1.txt` - Part 1 puzzle description

## Problem Overview

The movie theater has a tile floor with red tiles at specific coordinates. The challenge is to find the **largest rectangle** that can be formed using any two red tiles as opposite corners.

### Key Concepts

- Red tiles are given as (x, y) coordinates on a grid
- Any two red tiles can serve as opposite corners of a rectangle
- **Important**: We're counting grid cells, not geometric distance!
- Rectangle area = (|x₂ - x₁| + 1) × (|y₂ - y₁| + 1)
- Goal: Find the maximum possible area

### Example

Given red tiles at:
```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

The largest rectangle has area **50**, formed between tiles at (2,5) and (11,1):
- Columns: from 2 to 11 = 10 cells (2,3,4,5,6,7,8,9,10,11)
- Rows: from 1 to 5 = 5 cells (1,2,3,4,5)
- Width = |11 - 2| + 1 = 10
- Height = |5 - 1| + 1 = 5
- Area = 10 × 5 = 50 ✓

The "+1" is crucial because we're counting grid cells, not measuring distance!

## Setup

### File Structure

```
day 9/
├── README.md
├── day9_movie_theater.py
├── input.txt
└── day9part1.txt
```

### Requirements

- Python 3.x
- No external libraries required (uses only standard library)

## How to Run

Make sure you're in the `day 9` directory, then run:

```bash
python3 day9_movie_theater.py
```

Or if the script is executable:

```bash
./day9_movie_theater.py
```

## Expected Output

```
Number of red tiles: 496

Largest rectangle area: 4750092396
Corners: (85024, 83904) and (15221, 15856)

Answer: 4750092396
```

## Algorithm Details

### Approach: Brute Force with All Pairs

The solution uses a straightforward O(n²) algorithm:

1. **Parse Input**: Read all red tile coordinates from `input.txt`
2. **Check All Pairs**: For each pair of tiles (i, j):
   - Calculate rectangle width: |x₂ - x₁| + 1 (counting cells, not distance)
   - Calculate rectangle height: |y₂ - y₁| + 1 (counting cells, not distance)
   - Calculate area: width × height
3. **Track Maximum**: Keep track of the maximum area found
4. **Return Result**: Output the largest rectangle area

### Complexity Analysis

- **Time Complexity**: O(n²) where n is the number of red tiles
  - With 496 tiles, this is approximately 122,880 comparisons
  - Very fast for this problem size (runs in < 1 second)

- **Space Complexity**: O(n) to store the tile coordinates
  - Plus O(1) for tracking the maximum

### Why This Approach Works

- Since we can use ANY two red tiles as opposite corners, we need to consider all possible pairs
- There's no way to prune the search space without checking pairs
- The rectangle doesn't need to contain only red tiles - just have red tiles at two opposite corners
- This is optimal for this problem type

## Solution Verification

For the given input:
- **Number of tiles**: 496
- **Largest area**: 4,750,092,396
- **Corners**: (85024, 83904) and (15221, 15856)
- **Width**: |85024 - 15221| + 1 = 69,804 cells
- **Height**: |83904 - 15856| + 1 = 68,049 cells
- **Verification**: 69,804 × 68,049 = 4,750,092,396 ✓

### Common Mistake

Don't forget the "+1" when counting grid cells! The geometric distance between coordinates is different from the number of cells they span.
