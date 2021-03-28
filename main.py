import math
from random import random

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
        for index in range(1):
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
        star1 = a.AStar(puzzle1, 0)
        star2 = a.AStar(puzzle2, 0)
        solvable1 = star1.solve(1)
        solvable2 = star2.solve(2)
        solvable1 = False
        solved += 1
        print(f"=========solved: {solved}=========")


def depth_test(puzzles):
    for puzzle in puzzles:
        depth_first = df.DepthFirst(puzzle)
        depth_first.solve()
        depth_first.print_paths()


def iterative_deepening_test(puzzles):
    total_length_of_the_solution_paths = 0
    total_length_of_the_search_paths = 0
    total_number_of_no_solution = 0
    total_execution_time = 0
    for index, puzzle in enumerate(puzzles):
        iterative_deepening = itdeep.IterativeDeepening(p.Puzzle(puzzle), index)
        iterative_deepening.solve()
        iterative_deepening.print_paths()

        total_length_of_the_solution_paths += iterative_deepening.total_length_of_the_solution_path
        total_length_of_the_search_paths += iterative_deepening.total_length_of_the_search_path
        total_number_of_no_solution += 0 if iterative_deepening.solved else 1
        total_execution_time += iterative_deepening.execution_time

    print_analysis(len(puzzles), total_execution_time, total_length_of_the_search_paths, total_length_of_the_solution_paths,
                   total_number_of_no_solution)


def print_analysis(puzzle_count, total_execution_time, total_length_of_the_search_paths, total_length_of_the_solution_paths,
                   total_number_of_no_solution):
    print(f"\nTotal length of the solution paths = {total_length_of_the_solution_paths}")
    print(f"Average length of the solution paths = {total_length_of_the_solution_paths / (puzzle_count - total_number_of_no_solution if puzzle_count - total_number_of_no_solution > 0 else 1)}")
    print(f"\nTotal length of the search paths = {total_length_of_the_search_paths}")
    print(f"Average length of the search paths = {total_length_of_the_search_paths / puzzle_count}")
    print(f"\nTotal number of no solution = {total_number_of_no_solution}")
    print(f"Average number of no solution = {total_number_of_no_solution / puzzle_count}")
    print(f"\nTotal execution time = {total_execution_time} seconds")
    print(f"Average execution time = {total_execution_time / puzzle_count} seconds")


if __name__ == "__main__":
    main()
