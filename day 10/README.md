# Advent of Code 2025 - Day 10: Factory

Solution for [Advent of Code 2025 Day 10](https://adventofcode.com/2025/day/10)

## Files

- `day10_factory.py` - Python script that solves the challenge
- `input.txt` - Puzzle input (167 machines)
- `day10part1.txt` - Problem description
- `example.txt` - Generated example file for validation

## Problem Overview

Factory machines need to be initialized by configuring their indicator lights to match specific patterns. Each machine has:
- **Indicator lights** (initially all OFF): Need to match a target pattern
- **Buttons**: Each toggles specific lights when pressed
- **Goal**: Find the minimum number of button presses to configure all machines

### Key Concepts

1. **Light States**: Lights are binary (OFF=`.` or ON=`#`)
2. **Toggle Operation**: Pressing a button flips each of its assigned lights (OFF→ON or ON→OFF)
3. **XOR Property**: Pressing the same button twice cancels out (returns to original state)
4. **Optimization**: We only need to consider pressing each button 0 or 1 times (not 2+)

### Example

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

- **Target**: `[.##.]` = lights 0,1,2,3 should be OFF,ON,ON,OFF
- **Buttons**: 6 buttons available
  - Button 1: toggles light 3
  - Button 2: toggles lights 1,3
  - Button 3: toggles light 2
  - Button 4: toggles lights 2,3
  - Button 5: toggles lights 0,2
  - Button 6: toggles lights 0,1
- **Solution**: Press buttons 5 and 6 (2 presses total)
  - Button 5 toggles 0,2: `[#.#.]`
  - Button 6 toggles 0,1: `[.##.]` ✓

## Setup

### File Structure

```
day 10/
├── README.md
├── day10_factory.py
├── input.txt
└── day10part1.txt
```

### Requirements

- Python 3.x
- No external libraries required (uses only standard library)

## How to Run

```bash
cd "day 10"
python3 day10_factory.py
```

Or if executable:

```bash
./day10_factory.py
```

## Expected Output

### Example Validation
```
============================================================
Testing with example:
============================================================
Machine 1: 2 presses (4 lights, 6 buttons)
Machine 2: 3 presses (5 lights, 5 buttons)
Machine 3: 2 presses (6 lights, 4 buttons)

Example total: 7 presses for 3 machines
Expected: 7 presses
```

### Actual Result
```
============================================================
Solving actual input:
============================================================
Machine 1: 1 presses (7 lights, 8 buttons)
Machine 2: 1 presses (9 lights, 7 buttons)
...
Machine 167: 5 presses (10 lights, 12 buttons)

============================================================
ANSWER: 455 total button presses for 167 machines
============================================================
```

## Algorithm Details

### Mathematical Foundation

This is a **linear algebra problem over GF(2)** (Galois Field with 2 elements, i.e., mod 2 arithmetic):

1. Each button press is a binary vector representing which lights it toggles
2. Light state after pressing buttons is XOR of all pressed button vectors
3. Since XOR is self-inverse, pressing a button twice = not pressing it
4. We only need to find which subset of buttons to press (each 0 or 1 times)

### Implementation Strategy

**Brute Force with Bitmasking**:

1. **For each machine**:
   - Parse target pattern and button configurations
   - Generate all possible button combinations (2^n where n = number of buttons)
   - For each combination:
     - Simulate pressing those buttons (XOR their toggle patterns)
     - Check if result matches target
     - Track minimum number of buttons needed

2. **Representation**:
   - Use bitmask to represent button combinations
   - Bit i = 1 means press button i, 0 means don't press
   - Example: mask = 0b101 = press buttons 0 and 2

3. **Optimization**:
   - Early termination when solution with k presses found
   - Skip combinations with more than current minimum

### Complexity Analysis

**Per Machine**:
- **Time**: O(2^b × l) where b = buttons, l = lights
  - Try 2^b combinations
  - Each takes O(l) to verify
- **Space**: O(l) for storing light states

**Overall**:
- **Input**: 167 machines, max 13 buttons per machine
- **Worst case**: 2^13 = 8,192 combinations per machine
- **Practical**: Most machines have 6-10 buttons (64-1024 combinations)
- **Total runtime**: < 1 second

### Why This Approach Works

1. **Correctness**: We exhaustively try all combinations, guaranteed to find optimal
2. **Feasibility**: Small button counts (≤13) make brute force practical
3. **No need for Gaussian elimination**: Problem size small enough for enumeration
4. **XOR property**: Ensures we only need to consider 0/1 presses per button

## Solution Verification

For the given input:
- **Total machines**: 167
- **Total button presses**: 455
- **Average per machine**: ~2.72 presses
- **Range**: 1-8 presses per machine
- **Most common**: 2-3 presses per machine

### Example Machine Breakdown

Machine 7 (10 lights, 13 buttons):
- Target: `[#####.###.]`
- Only **1 button press** needed (optimal)
- Despite having 8,192 possible combinations!

Machine 80 (9 lights, 9 buttons):
- Target: Complex 9-light pattern
- Needs **8 button presses** (maximum in dataset)
- Shows problem can require many buttons

## Alternative Approaches (Not Used)

1. **Gaussian Elimination over GF(2)**:
   - More complex to implement
   - Would find *a* solution but not necessarily minimum
   - Would need additional optimization step

2. **BFS/Dijkstra**:
   - Explore state space of light configurations
   - Could work but higher complexity
   - State space = 2^l (exponential in lights, not buttons)

3. **Dynamic Programming**:
   - Possible but no clear subproblem structure
   - Current brute force simpler and fast enough

The brute force approach is ideal here due to small problem size (≤13 buttons).
