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
    depth_test(puzzles)
    # iterative_deepening_test(puzzles)


def generate_puzzle_file():
    with open("puzzles.txt", "w") as f:
        for index in range(20):
            s_puzzle = p.generate_puzzle(3)
            f.write(s_puzzle)
            f.write("\n")


def read_puzzle_file():
    puzzles = []
    with open("puzzles.txt", "r") as f:
        for line in f:
            puzzles.append(p.convert_puzzle_input(line))
    return puzzles


def test():
    total_solved = 0
    for n in range(25, 30):
        s_puzzle = p.generate_puzzle(n)
        s_puzzle = p.convert_puzzle_input(s_puzzle)
        print(f"matrix: {n}x{n}")
        puzzle = p.Puzzle(s_puzzle)
        star = a.AStar(puzzle, 0)
        solved = star.start(2)
        if not solved:
            print(f"not solved:\n{star.puzzle.initial_state}")
            break
        print(f"solved: {solved}")
        print(f"time: {star.get_total_time()}")
        print(f"swaps: {star.total_swaps}")
        total_solved += 1
        print(f"======== total solved: {total_solved} ========")
    # solvable1 = True
    # solvable2 = True
    # solved = 0
    # while solvable1 and solvable2:
    #     s_puzzle = p.generate_puzzle()
    #     s_puzzle = p.convert_puzzle_input(s_puzzle)
    #     print(f"initial: \n{np.array(s_puzzle)}")
    #     puzzle1 = p.Puzzle(s_puzzle)
    #     puzzle2 = p.Puzzle(s_puzzle)
    #     star1 = a.AStar(puzzle1, 0)
    #     star2 = a.AStar(puzzle2, 0)
    #     # solvable1 = star1.start(1)
    #     solvable2 = star2.start(2)
    #     # print(f"time1: {star1.get_total_time()}")
    #     print(f"time2: {star2.get_total_time()}")
    #     # print(f"swaps1: {star1.total_swaps}")
    #     print(f"swaps2: {star2.total_swaps}")
    #     # solvable2 = False
    #     solved += 1
    #     print(f"=========solved: {solved}=========")


def depth_test(puzzles):
    total_length_of_the_solution_paths = 0
    total_length_of_the_search_paths = 0
    total_number_of_no_solution = 0
    total_execution_time = 0
    for index, puzzle in enumerate(puzzles):
        depth_first = df.DepthFirst(p.Puzzle(puzzle), index)
        depth_first.solve()
        depth_first.print_paths()

        total_length_of_the_solution_paths += depth_first.total_length_of_the_solution_path
        total_length_of_the_search_paths += depth_first.total_length_of_the_search_path
        total_number_of_no_solution += 0 if depth_first.solved else 1
        total_execution_time += depth_first.execution_time

    print_analysis(len(puzzles), total_execution_time, total_length_of_the_search_paths, total_length_of_the_solution_paths,
                   total_number_of_no_solution)


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
