import time

import puzzle as p
import astar as a
import numpy as np
import depthfirst as df


def main():
    # test()
    depth_test()


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


def depth_test():
    s_puzzle = p.generate_puzzle()
    s_puzzle = p.convert_puzzle_input(s_puzzle)

    puzzle = p.Puzzle(s_puzzle)
    depth_first = df.DepthFirst(puzzle)
    start_time = time.time()
    try:
        depth_first.solve()
    except KeyboardInterrupt:
        pass
    current_time = time.time()
    elapsed_time = current_time - start_time
    print(elapsed_time)
    depth_first.print_paths()


if __name__ == "__main__":
    main()
