import puzzle as p


def main():
    s_puzzle = p.generate_puzzle()
    print("s_puzzle: ", s_puzzle)

    s_puzzle = p.convert_puzzle_input(s_puzzle)
    print("s_puzzle: ", s_puzzle)

    puzzle = p.Puzzle(s_puzzle)
    adjacent_test(puzzle)


def adjacent_test(puzzle):
    print(f"puzzle: \n{puzzle.get_puzzle()}")
    print(f"element: {puzzle.get_puzzle()[1][1]}")
    print(f"top: {puzzle.get_top(1, 1)} at {puzzle.get_top_index(1, 1)}")
    print(f"left: {puzzle.get_left(1, 1)} at {puzzle.get_left_index(1, 1)}")
    print(f"right: {puzzle.get_right(1, 1)} at {puzzle.get_right_index(1, 1)}")
    print(f"bottom: {puzzle.get_bottom(1, 1)} at {puzzle.get_bottom_index(1, 1)}")


if __name__ == "__main__":
    main()
