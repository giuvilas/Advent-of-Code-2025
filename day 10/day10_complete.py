#!/usr/bin/env python3

"""
Day 10: Factory - Complete Solution for Both Parts

Part 1: Toggle lights to match pattern (Gaussian elimination over GF(2))
Part 2: Add to counters to reach targets (Integer Linear Programming)
"""

import re
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

def parse_line(line):
    """Parse a single machine line."""
    indicator_match = re.search(r'\[([.#]+)\]', line)
    indicator = indicator_match.group(1) if indicator_match else ""

    buttons = re.findall(r'\(([0-9,]+)\)', line)
    buttons = [list(map(int, b.split(','))) for b in buttons]

    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    targets = list(map(int, joltage_match.group(1).split(',')))

    return indicator, buttons, targets

def solve_machine_part1(buttons, target_pattern):
    """
    Part 1: Toggle lights to match pattern using minimum button presses.
    Uses Gaussian elimination over GF(2) (binary field).
    """
    n_buttons = len(buttons)
    n_lights = len(target_pattern)
    target = [1 if c == '#' else 0 for c in target_pattern]

    # Build augmented matrix [A | target] over GF(2)
    matrix = []
    for i in range(n_lights):
        row = [1 if i in buttons[j] else 0 for j in range(n_buttons)]
        row.append(target[i])
        matrix.append(row)

    # Gaussian elimination over GF(2)
    pivot_cols = []
    row = 0
    for col in range(n_buttons):
        # Find pivot
        pivot_row = None
        for r in range(row, n_lights):
            if matrix[r][col] == 1:
                pivot_row = r
                break
        if pivot_row is None:
            continue

        pivot_cols.append(col)
        matrix[row], matrix[pivot_row] = matrix[pivot_row], matrix[row]

        # Eliminate
        for r in range(n_lights):
            if r != row and matrix[r][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[r][c] ^= matrix[row][c]
        row += 1

    # Find minimum solution by trying all free variables
    free_cols = [c for c in range(n_buttons) if c not in pivot_cols]
    min_presses = float('inf')

    for mask in range(1 << len(free_cols)):
        solution = [0] * n_buttons
        for i, col in enumerate(free_cols):
            solution[col] = (mask >> i) & 1

        for i, pivot_col in enumerate(pivot_cols):
            val = matrix[i][-1]
            for c in range(pivot_col + 1, n_buttons):
                val ^= matrix[i][c] * solution[c]
            solution[pivot_col] = val

        presses = sum(solution)
        min_presses = min(min_presses, presses)

    return min_presses

def solve_machine_part2(buttons, targets):
    """
    Part 2: Add to counters to reach exact targets with minimum presses.
    Uses Integer Linear Programming via scipy.optimize.milp.
    """
    n_buttons = len(buttons)
    n_counters = len(targets)

    # Build constraint matrix: A[counter][button] = 1 if button affects counter
    A = np.zeros((n_counters, n_buttons))
    for j, button in enumerate(buttons):
        for counter in button:
            if counter < n_counters:
                A[counter][j] = 1

    # Objective: minimize sum of button presses
    c = np.ones(n_buttons)

    # Constraints: A * x = targets (exact equality)
    constraints = LinearConstraint(A, targets, targets)

    # Bounds: each button pressed 0 or more times
    bounds = Bounds(lb=0, ub=np.inf)

    # Solve with integer constraint
    result = milp(c, constraints=constraints, bounds=bounds,
                  integrality=np.ones(n_buttons))

    if result.success:
        return int(round(result.fun))
    return -1

def solve(input_text):
    """Solve both parts."""
    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]

    total_part1 = 0
    total_part2 = 0

    for i, line in enumerate(lines, 1):
        indicator, buttons, targets = parse_line(line)
        p1 = solve_machine_part1(buttons, indicator)
        p2 = solve_machine_part2(buttons, targets)

        total_part1 += p1
        total_part2 += p2

        print(f"Machine {i}: Part1={p1}, Part2={p2}")

    return total_part1, total_part2

if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        puzzle_input = f.read()

    part1, part2 = solve(puzzle_input)

    print("\n" + "=" * 60)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print("=" * 60)
