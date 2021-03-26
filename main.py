import puzzle as p
import numpy as np


def main():
    s_puzzle = p.generate_puzzle()
    print("s_puzzle: ", s_puzzle)

    s_puzzle = p.convert_puzzle_input(s_puzzle)
    print("s_puzzle: ", s_puzzle)

    puzzle = p.Puzzle(s_puzzle)
    test(puzzle)


def test(puzzle):
    print("=================")
    value = 1
    row = puzzle.get_row_of(value)
    col = puzzle.get_col_of(value)
    print(f"puzzle: \n{puzzle.get_puzzle()}")
    print(f"value: {value} at {puzzle.get_index_of(value)}")
    print(f"top: {puzzle.get_top(value)} at {puzzle.get_top_index(value)}")
    print(f"left: {puzzle.get_left(value)} at {puzzle.get_left_index(value)}")
    print(f"right: {puzzle.get_right(value)} at {puzzle.get_right_index(value)}")
    print(f"bottom: {puzzle.get_bottom(value)} at {puzzle.get_bottom_index(value)}")
    print(f"get value at {row, col} : {puzzle.get_value_at(row, col)}")

    print("=============")
    value1 = 5
    value2 = 1
    print(f"puzzle: \n{puzzle.get_puzzle()}")
    print(f"adjacent to {value1}: {puzzle.get_adjacent(value1)}")
    print(f"{value1} is adjacent to {value2}: {puzzle.is_adjacent(value1, value2)}")

    print("==========")
    print(f"swap {value1} and {value2}")
    print(f"{puzzle.swap(value1, value2)}")
    print(f"{puzzle.get_puzzle()}")

    print(f"goal: \n{puzzle.goal_state}")


if __name__ == "__main__":
    main()
