#!/usr/bin/env python3

"""
Day 10 Part 2: Mathematical approach using matrix solving

Since this is a system of linear equations A*x = b where we want to
minimize sum(x), we can try to solve it mathematically.

For small problems, we can try all reasonable combinations.
"""

import re
from itertools import product


def parse_machine(line):
    """Parse a machine line to extract joltage targets and button configs."""
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    if not joltage_match:
        return None, None

    joltage_str = joltage_match.group(1)
    targets = [int(x) for x in joltage_str.split(',')]
    num_counters = len(targets)

    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    return targets, buttons, num_counters


def bruteforce_bounded(targets, buttons, num_counters):
    """
    Brute force with bounded search space.

    For each button, we know it can be pressed at most max(targets) times.
    Try all combinations within reasonable bounds.
    """
    max_target = max(targets)
    num_buttons = len(buttons)

    # Upper bound: each button pressed at most max_target times
    # But realistically, total presses <= sum(targets) / min_buttons_per_counter
    max_total = sum(targets) * 2  # Generous upper bound

    # Try combinations with increasing total presses
    for total_presses in range(sum(targets) // 2, max_total):
        # Try all ways to distribute total_presses among buttons
        # This is still exponential, but we can limit search

        # Use a simpler approach: try combinations where each button
        # is pressed 0 to min(target_max, total_presses) times
        max_per_button = min(max_target, total_presses)

        # Too many combinations if we try all - let's use a heuristic
        # Try reasonable distributions
        for combo in _generate_combinations(num_buttons, total_presses, max_per_button):
            # Check if this combination reaches targets
            current = [0] * num_counters
            for button_idx, times in enumerate(combo):
                for counter_idx in buttons[button_idx]:
                    current[counter_idx] += times

            if current == targets:
                return total_presses

    return -1


def _generate_combinations(num_buttons, total, max_per):
    """Generate combinations of button presses that sum to total."""
    # This is still too slow for large cases
    # Use a pruned search
    if num_buttons == 1:
        if total <= max_per:
            yield [total]
        return

    for first in range(min(total + 1, max_per + 1)):
        for rest in _generate_combinations(num_buttons - 1, total - first, max_per):
            yield [first] + rest


def solve_factory_part2(filename):
    """Solve all machines for Part 2."""
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
            print(f"Machine {machine_count}: Solving...", flush=True)

            min_presses = bruteforce_bounded(targets, buttons, num_counters)

            print(f"Machine {machine_count}: {min_presses} presses")
            total_presses += min_presses

    return total_presses, machine_count


def main():
    print("=" * 60)
    print("Testing with example:")
    print("=" * 60)

    example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    with open('example_part2.txt', 'w') as f:
        f.write(example)

    total, count = solve_factory_part2('example_part2.txt')
    print(f"\nExample total: {total}")
    print(f"Expected: 33")


if __name__ == "__main__":
    main()
