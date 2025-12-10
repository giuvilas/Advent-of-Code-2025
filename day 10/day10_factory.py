#!/usr/bin/env python3

"""
Day 10: Factory - Minimum Button Presses

Each machine has indicator lights (initially OFF) that need to match a target.
Buttons toggle specific lights. Find minimum button presses needed.

Key insight: Since toggling is XOR, pressing a button twice = no press.
We only need to consider each button pressed 0 or 1 times.

This becomes: Find the subset of buttons with minimum size such that
XORing their toggle patterns produces the target pattern.
"""

import re


def parse_machine(line):
    """
    Parse a machine line to extract:
    - target: list of bools (True = light ON in target)
    - buttons: list of lists (each button's light indices)
    """
    # Extract pattern in [square brackets]
    pattern_match = re.search(r'\[([.#]+)\]', line)
    if not pattern_match:
        return None, None

    pattern_str = pattern_match.group(1)
    target = [c == '#' for c in pattern_str]
    num_lights = len(target)

    # Extract all button configurations in (parentheses)
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    return target, buttons, num_lights


def apply_buttons(button_combination, buttons, num_lights):
    """
    Apply a combination of buttons and return resulting light state.
    button_combination: list of bools (True = press that button)
    """
    lights = [False] * num_lights

    for i, should_press in enumerate(button_combination):
        if should_press:
            # Toggle lights for this button
            for light_idx in buttons[i]:
                lights[light_idx] = not lights[light_idx]

    return lights


def find_min_presses(target, buttons, num_lights):
    """
    Find minimum number of button presses to achieve target state.

    Strategy: Try all possible combinations of buttons (2^n possibilities)
    and find the one with minimum number of presses that achieves target.
    """
    num_buttons = len(buttons)
    min_presses = float('inf')

    # Try all possible combinations (each button pressed 0 or 1 times)
    for mask in range(1 << num_buttons):  # 2^num_buttons combinations
        # Build button combination from mask
        combination = [(mask >> i) & 1 for i in range(num_buttons)]

        # Check if this combination achieves target
        result = apply_buttons(combination, buttons, num_lights)

        if result == target:
            # Count number of button presses
            presses = sum(combination)
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else 0


def solve_factory(filename):
    """
    Solve all machines and return total minimum button presses.
    """
    total_presses = 0
    machine_count = 0

    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            target, buttons, num_lights = parse_machine(line)
            if target is None:
                continue

            machine_count += 1
            min_presses = find_min_presses(target, buttons, num_lights)

            print(f"Machine {machine_count}: {min_presses} presses "
                  f"({num_lights} lights, {len(buttons)} buttons)")

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

    with open('example.txt', 'w') as f:
        f.write(example)

    total, count = solve_factory('example.txt')
    print(f"\nExample total: {total} presses for {count} machines")
    print(f"Expected: 7 presses")
    print()

    # Solve actual input
    print("=" * 60)
    print("Solving actual input:")
    print("=" * 60)

    total, count = solve_factory('input.txt')

    print("\n" + "=" * 60)
    print(f"ANSWER: {total} total button presses for {count} machines")
    print("=" * 60)


if __name__ == "__main__":
    main()
