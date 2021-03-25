import puzzle as p


def main():
    s_puzzle = p.generate_puzzle()
    print("s_puzzle: ", s_puzzle)

    s_puzzle = p.convert_puzzle_input(s_puzzle)
    print("s_puzzle: ", s_puzzle)

    puzzle = p.Puzzle(s_puzzle)
    adjacent_test(puzzle)


def adjacent_test(puzzle):
    print("puzzle: ", puzzle.get_puzzle())
    print("top: ", puzzle.get_adjacent_top(1, 1))
    print("left: ", puzzle.get_adjacent_left(1, 1))
    print("right: ", puzzle.get_adjacent_right(1, 1))
    print("bottom: ", puzzle.get_adjacent_bottom(1, 1))

    print("================")
    print("top: ", puzzle.get_adjacent_top(0, 0))
    print("left: ", puzzle.get_adjacent_left(0, 0))
    print("right: ", puzzle.get_adjacent_right(0, 0))
    print("bottom: ", puzzle.get_adjacent_bottom(0, 0))
    print("================")
    print("top: ", puzzle.get_adjacent_top(0, 1))
    print("left: ", puzzle.get_adjacent_left(0, 1))
    print("right: ", puzzle.get_adjacent_right(0, 1))
    print("bottom: ", puzzle.get_adjacent_bottom(0, 1))
    print("================")
    print("top: ", puzzle.get_adjacent_top(0, 2))
    print("left: ", puzzle.get_adjacent_left(0, 2))
    print("right: ", puzzle.get_adjacent_right(0, 2))
    print("bottom: ", puzzle.get_adjacent_bottom(0, 2))
    print("================")
    print("top: ", puzzle.get_adjacent_top(2, 2))
    print("left: ", puzzle.get_adjacent_left(2, 2))
    print("right: ", puzzle.get_adjacent_right(2, 2))
    print("bottom: ", puzzle.get_adjacent_bottom(2, 2))
    print("================")
    print("top: ", puzzle.get_adjacent_top(3, 5))
    print("left: ", puzzle.get_adjacent_left(3, 5))
    print("right: ", puzzle.get_adjacent_right(3, 5))
    print("bottom: ", puzzle.get_adjacent_bottom(3, 5))


if __name__ == "__main__":
    main()
