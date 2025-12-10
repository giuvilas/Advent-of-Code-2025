# Day 10 Part 2: Analysis and Solution Approach

## Problem Transformation

Part 2 is fundamentally different from Part 1:
- **Part 1**: Binary toggle problem (XOR over GF(2))
- **Part 2**: Integer counter problem (linear Diophantine equations)

## Mathematical Formulation

This is an **Integer Linear Programming** (ILP) problem:

**Minimize**: Σ x_i (total button presses)
**Subject to**: A × x = b, where x_i ≥ 0, x_i ∈ ℤ

Where:
- x = vector of button press counts
- A = button-to-counter incidence matrix (A[j][i] = 1 if button i affects counter j)
- b = target joltage vector

## Why Standard Approaches Are Slow

### State Space Explosion
- BFS/A* state space = product of (target_i + 1) for all counters
- Example: {67,29,30,40,18,54,21} → 68×30×31×41×19×55×22 ≈ 10^12 states!

### Greedy Pitfalls
- Greedy algorithms can get stuck (overshoot some counters while others are incomplete)
- No guarantee of optimality
- May fail to find solutions even when they exist

## Solution Approaches

### 1. A* Search (Implemented)
- **Works for**: Small target values (≤15)
- **Heuristic**: Sum of remaining needed increments (admissible)
- **Optimization**: Prune states that overshoot any target
- **Limitation**: Exponential state space for large values

### 2. Integer Linear Programming (Optimal but requires libraries)
- Use `scipy.optimize.linprog` with `integrality` constraints
- Or `pulp` library for ILP
- **Not available** in standard Python installation

### 3. Branch and Bound (Theoretical)
- Solve LP relaxation (fractional button presses allowed)
- Branch on fractional variables
- **Complex to implement from scratch**

### 4. Dynamic Programming (Possible)
- State = (remaining targets)
- But state space still exponential in target values

## Example Analysis

### Machine 1: {3,5,4,7}
Buttons: (3), (1,3), (2), (2,3), (0,2), (0,1)

Optimal solution (10 presses):
- Button (3): 1 press → counter 3 += 1
- Button (1,3): 3 presses → counter 1 += 3, counter 3 += 3
- Button (2,3): 3 presses → counter 2 += 3, counter 3 += 3
- Button (0,2): 1 press → counter 0 += 1, counter 2 += 1
- Button (0,1): 2 presses → counter 0 += 2, counter 1 += 2

Result: [3, 5, 4, 7] ✓

### Key Insight
Sum of targets = 19, optimal = 10
Many buttons affect 2 counters → roughly targets/2 presses needed

## Recommendation for Full Solution

For Advent of Code, this problem likely expects either:
1. **External library** (scipy/pulp for ILP)
2. **Clever mathematical insight** we haven't discovered
3. **Specialized algorithm** for this specific constraint structure

## Implemented Solutions

- `day10_part2.py` - A* search (works for small examples)
- `day10_part2_greedy.py` - Greedy approach (fails on many cases)
- `day10_part2_math.py` - Bounded search (too slow for large inputs)

## Partial Results

With A* on examples:
- Example 1: Computing... (slow)
- Example 2: Computing... (slow)
- Example 3: Computing... (slow)

The algorithm is correct but computationally infeasible for larger values.

## Future Work

To solve completely:
1. Install `scipy` or `pulp` for ILP solving
2. Implement sophisticated branch-and-bound from scratch
3. Discover problem-specific optimization
