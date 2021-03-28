import puzzle as p
import astar as a
import numpy as np
import depthfirst as df
import iterativedeepening as itdeep


def main():
    generate_puzzle_file()
    puzzles = read_puzzle_file()
    # test(puzzles)
    # depth_test(puzzles)
    iterative_deepening_test(puzzles)


def generate_puzzle_file():
    with open("puzzles.txt", "w") as f:
        for index in range(20):
            s_puzzle = p.generate_puzzle()
            f.write(s_puzzle)
            f.write("\n")


def read_puzzle_file():
    puzzles = []
    with open("puzzles.txt", "r") as f:
        for line in f:
            puzzles.append(p.convert_puzzle_input(line))
    return puzzles


def test():
    solvable1 = True
    solvable2 = True
    solved = 0
    while solvable1 and solvable2:
        s_puzzle = p.generate_puzzle()
        s_puzzle = p.convert_puzzle_input(s_puzzle)
        print(f"initial: \n{np.array(s_puzzle)}")
        puzzle1 = p.Puzzle(s_puzzle)
        puzzle2 = p.Puzzle(s_puzzle)
        star1 = a.AStar(puzzle1)
        star2 = a.AStar(puzzle2)
        solvable1 = star1.solve(1)
        solvable2 = star2.solve(2)
        solved += 1
        print(f"=========solved: {solved}=========")


def depth_test(puzzles):
    for puzzle in puzzles:
        depth_first = df.DepthFirst(puzzle)
        depth_first.solve()
        depth_first.print_paths()


def iterative_deepening_test(puzzles):
    for index, puzzle in enumerate(puzzles):
        iterative_deepening = itdeep.IterativeDeepening(p.Puzzle(puzzle), index)
        iterative_deepening.solve()
        iterative_deepening.print_paths()


if __name__ == "__main__":
    main()
