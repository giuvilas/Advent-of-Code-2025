#!/usr/bin/env python3

"""
Day 10 Part 2: Factory - Minimum Button Presses for Joltage

Counters start at 0. Buttons ADD 1 to specified counters.
Find minimum button presses to reach exact target joltage values.

This is an Integer Linear Programming problem:
- Minimize: sum(button_presses)
- Subject to: A * x = target, x_i >= 0, x_i ∈ Z

Algorithm: BFS with state space search and pruning
"""

import re
from collections import deque
import heapq


def parse_machine(line):
    """Parse a machine line to extract joltage targets and button configs."""
    # Extract joltage requirements in {curly braces}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    if not joltage_match:
        return None, None

    joltage_str = joltage_match.group(1)
    targets = [int(x) for x in joltage_str.split(',')]
    num_counters = len(targets)

    # Extract all button configurations in (parentheses)
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    return targets, buttons, num_counters


def heuristic(state, targets):
    """
    Heuristic: sum of remaining values needed for each counter.
    This is admissible (never overestimates) since each button press
    can add at most 1 to each counter.
    """
    return sum(max(0, targets[i] - state[i]) for i in range(len(state)))


def astar_min_presses(targets, buttons, num_counters):
    """
    Find minimum button presses using A* search with pruning.

    State: tuple of current counter values
    Start: all zeros
    Goal: targets
    Action: press any button (increase relevant counters by 1)

    Heuristic: sum of remaining increments needed (admissible)
    Optimization: Don't explore states where any counter exceeds its target
    """
    start_state = tuple([0] * num_counters)
    target_state = tuple(targets)

    if start_state == target_state:
        return 0

    # Priority queue: (estimated_total, actual_presses, state)
    # estimated_total = actual_presses + heuristic
    h_start = heuristic(start_state, targets)
    heap = [(h_start, 0, start_state)]
    visited = {start_state: 0}  # state -> minimum presses to reach it

    while heap:
        est_total, presses, state = heapq.heappop(heap)

        # Check if we reached target
        if state == target_state:
            return presses

        # Skip if we've found a better path to this state
        if state in visited and visited[state] < presses:
            continue

        # Try pressing each button
        for button in buttons:
            # Calculate new state after pressing this button
            new_state = list(state)
            valid = True

            for counter_idx in button:
                new_state[counter_idx] += 1
                # Prune: don't exceed target
                if new_state[counter_idx] > targets[counter_idx]:
                    valid = False
                    break

            if not valid:
                continue

            new_state = tuple(new_state)
            new_presses = presses + 1

            # Only explore if we haven't visited or found a better path
            if new_state not in visited or visited[new_state] > new_presses:
                visited[new_state] = new_presses
                h = heuristic(new_state, targets)
                est = new_presses + h
                heapq.heappush(heap, (est, new_presses, new_state))

    # No solution found (shouldn't happen for valid inputs)
    return -1


def solve_factory_part2(filename):
    """Solve all machines for Part 2 and return total minimum button presses."""
    total_presses = 0
    machine_count = 0

    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            targets, buttons, num_counters = parse_machine(line)
            if targets is None:
                continue

            machine_count += 1
            min_presses = astar_min_presses(targets, buttons, num_counters)

            print(f"Machine {machine_count}: {min_presses} presses "
                  f"(targets: {targets}, {len(buttons)} buttons)")

            total_presses += min_presses

    return total_presses, machine_count


def main():
    # Test with example first
    print("=" * 60)
    print("Testing with example:")
    print("=" * 60)

    # Create example file
    example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    with open('example_part2.txt', 'w') as f:
        f.write(example)

    total, count = solve_factory_part2('example_part2.txt')
    print(f"\nExample total: {total} presses for {count} machines")
    print(f"Expected: 33 presses")
    print()

    # Solve actual input
    print("=" * 60)
    print("Solving actual input:")
    print("=" * 60)

    total, count = solve_factory_part2('input.txt')

    print("\n" + "=" * 60)
    print(f"ANSWER: {total} total button presses for {count} machines")
    print("=" * 60)


if __name__ == "__main__":
    main()
