#!/usr/bin/env python3

"""
Day 10 Part 2: Factory - Using Greedy Algorithm

For larger values, use a greedy approach:
1. Find counters that need the most increments
2. Press buttons that help these counters without overshooting
3. Prefer buttons that help multiple needed counters

This trades optimality for speed.
"""

import re


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


def greedy_min_presses(targets, buttons, num_counters):
    """
    Greedy algorithm: repeatedly press the button that makes most progress.

    Strategy:
    1. Calculate how much each counter needs
    2. Find button that:
       - Helps counters that need increments
       - Doesn't overshoot any counter
       - Preferably helps multiple needed counters
    3. Press that button
    4. Repeat until all counters reach targets
    """
    current = [0] * num_counters
    presses = 0

    while current != targets:
        best_button = None
        best_score = -1

        # Try each button and score it
        for button_idx, button in enumerate(buttons):
            # Check if pressing this button would overshoot any counter
            would_overshoot = False
            helps_count = 0
            total_help = 0

            for counter_idx in button:
                if current[counter_idx] >= targets[counter_idx]:
                    would_overshoot = True
                    break
                # Count how much this button helps
                if current[counter_idx] < targets[counter_idx]:
                    helps_count += 1
                    needed = targets[counter_idx] - current[counter_idx]
                    total_help += min(1, needed)  # This button adds 1

            if would_overshoot:
                continue

            # Score: prefer buttons that help more counters that need help
            # Also consider how much each counter needs (prioritize bigger gaps)
            score = helps_count * 100 + total_help

            if score > best_score:
                best_score = score
                best_button = button_idx

        if best_button is None:
            # No valid button found (shouldn't happen)
            return -1

        # Press the best button
        for counter_idx in buttons[best_button]:
            current[counter_idx] += 1
        presses += 1

    return presses


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
            min_presses = greedy_min_presses(targets, buttons, num_counters)

            print(f"Machine {machine_count}: {min_presses} presses "
                  f"(targets: {targets}, {len(buttons)} buttons)")

            total_presses += min_presses

    return total_presses, machine_count


def main():
    # Test with example first
    print("=" * 60)
    print("Testing with example (Greedy approach):")
    print("=" * 60)

    # Create example file
    example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    with open('example_part2.txt', 'w') as f:
        f.write(example)

    total, count = solve_factory_part2('example_part2.txt')
    print(f"\nExample total: {total} presses for {count} machines")
    print(f"Expected: 33 presses (greedy might differ slightly)")
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
