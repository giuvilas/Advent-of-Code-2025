# Advent of Code 2025 - Day 9: Movie Theater

Solution for [Advent of Code 2025 Day 9](https://adventofcode.com/2025/day/9)

## Files

- `day9_movie_theater.py` - Part 1 solution
- `day9_part2.py` - Part 2 solution
- `input.txt` - Puzzle input (496 red tile coordinates)
- `day9part1.txt` - Part 1 puzzle description
- `day9part2.txt` - Part 2 puzzle description
- `test_example.txt` - Example input for validation

## Problem Overview

The movie theater has a tile floor with red tiles at specific coordinates.

### Part 1
Find the **largest rectangle** that can be formed using any two red tiles as opposite corners.

### Part 2
The red tiles form a **closed polygon** (connected in list order). Green tiles fill:
- The edges connecting consecutive red tiles
- All tiles inside the polygon

Find the largest rectangle with red corners that is **entirely within the polygon** (only contains red/green tiles).

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

Make sure you're in the `day 9` directory.

### Part 1

```bash
python3 day9_movie_theater.py
```

### Part 2

```bash
python3 day9_part2.py
```

Or if the scripts are executable, use `./day9_movie_theater.py` or `./day9_part2.py`

## Expected Output

### Part 1

```
Number of red tiles: 496

Largest rectangle area: 4750092396
Corners: (85024, 83904) and (15221, 15856)

Answer: 4750092396
```

### Part 2

```
Number of red tiles (polygon vertices): 496

Checking 122760 rectangle candidates...
Progress: 0/496 tiles checked...
  [Progress updates as it finds larger rectangles...]
Progress: 450/496 tiles checked...
Checked 31308 candidate rectangles

============================================================
Largest valid rectangle area: 4606686568
Corners: (15065, 83109) and (84782, 17034)

Answer: 4606686568
```

## Algorithm Details

### Part 1: Brute Force with All Pairs

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

### Part 2: Polygon Constraint with Point-in-Polygon Testing

Part 2 adds a significant constraint - the rectangle must be entirely within the polygon:

1. **Build Polygon**: Red tiles form a closed polygon (in input order)
2. **Point-in-Polygon Test**: Implement ray casting algorithm to check if points are inside
3. **Validate Rectangles**: For each red tile pair:
   - Calculate potential area
   - Skip if it can't beat current maximum (optimization)
   - Check if all corners are inside/on polygon
   - Sample edge and interior points for large rectangles
   - Track maximum valid area
4. **Return Result**: Output largest valid rectangle

**Key Optimizations**:
- Only check rectangles that could beat the current max
- Sample points intelligently (corners + edges + center)
- Early termination when checking validity

**Complexity**:
- Time: O(n² × m) where n = tiles, m = polygon vertices for each point test
- With 496 tiles, checks ~122k candidates, validates ~31k promising ones
- Runs in ~10-20 seconds

## Solution Verification

### Part 1
- **Largest area**: 4,750,092,396
- **Corners**: (85024, 83904) and (15221, 15856)
- **Width**: 69,804 cells | **Height**: 68,049 cells
- **Verification**: 69,804 × 68,049 = 4,750,092,396 ✓

### Part 2
- **Largest area**: 4,606,686,568
- **Corners**: (15065, 83109) and (84782, 17034)
- **Width**: 69,718 cells | **Height**: 66,076 cells
- **Verification**: 69,718 × 66,076 = 4,606,686,568 ✓
- **Note**: Smaller than Part 1 due to polygon constraint ✓

### Common Mistakes

1. **Part 1**: Don't forget the "+1" when counting grid cells! The geometric distance between coordinates is different from the number of cells they span.
2. **Part 2**: The polygon is formed by the tiles in list order - don't sort them!
