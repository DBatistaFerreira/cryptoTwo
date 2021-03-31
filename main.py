import puzzle as p
import astar as a
import depthfirst as df
import iterativedeepening as itdeep


def main():
    # generate_puzzle_file()

    puzzles = read_puzzle_file()

    depth_test(puzzles)
    iterative_deepening_test(puzzles)
    astar_test(puzzles)


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


def astar_test(puzzles):
    h1_total_length_of_the_solution_paths = 0
    h1_total_length_of_the_search_paths = 0
    h1_total_number_of_no_solution = 0
    h1_total_execution_time = 0
    h1_total_cost = 0
    h2_total_length_of_the_solution_paths = 0
    h2_total_length_of_the_search_paths = 0
    h2_total_number_of_no_solution = 0
    h2_total_execution_time = 0
    h2_total_cost = 0
    for puzzle_number, puzzle in enumerate(puzzles):
        ah1 = a.AStar(p.Puzzle(puzzle), puzzle_number)
        ah2 = a.AStar(p.Puzzle(puzzle), puzzle_number)
        h1_solved = ah1.solve(heuristic=1)
        h2_solved = ah2.solve(heuristic=2)
        h1_total_length_of_the_search_paths += ah1.total_length_of_search_path
        h2_total_length_of_the_search_paths += ah2.total_length_of_search_path
        h1_total_number_of_no_solution += 0 if h1_solved else 1
        h2_total_number_of_no_solution += 0 if h2_solved else 1
        h1_total_length_of_the_solution_paths += ah1.total_length_of_solution_path
        h2_total_length_of_the_solution_paths += ah2.total_length_of_solution_path
        h1_total_execution_time += ah1.total_time
        h2_total_execution_time += ah2.total_time
        h1_total_cost += ah1.total_cost
        h2_total_cost += ah2.total_cost

    print(f"======================================= h1 =======================================")
    print_analysis(len(puzzles), h1_total_execution_time, h1_total_length_of_the_search_paths,
                   h1_total_length_of_the_solution_paths, h1_total_number_of_no_solution, h1_total_cost)
    print(f"======================================= h1 =======================================")
    print(f"======================================= h2 =======================================")
    print_analysis(len(puzzles), h2_total_execution_time, h2_total_length_of_the_search_paths,
                   h2_total_length_of_the_solution_paths, h2_total_number_of_no_solution, h2_total_cost)
    print(f"======================================= h2 =======================================")
    print("done")


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

    print_analysis(len(puzzles), total_execution_time, total_length_of_the_search_paths,
                   total_length_of_the_solution_paths, total_number_of_no_solution)


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

    print_analysis(len(puzzles), total_execution_time, total_length_of_the_search_paths,
                   total_length_of_the_solution_paths, total_number_of_no_solution)


def print_analysis(puzzle_count, total_execution_time, total_length_of_the_search_paths,
                   total_length_of_the_solution_paths, total_number_of_no_solution, total_cost=None):
    print(f"\nTotal length of the solution paths = {total_length_of_the_solution_paths}")
    print(f"Average length of the solution paths = {total_length_of_the_solution_paths / (puzzle_count - total_number_of_no_solution if puzzle_count - total_number_of_no_solution > 0 else 1)}")
    print(f"\nTotal length of the search paths = {total_length_of_the_search_paths}")
    print(f"Average length of the search paths = {total_length_of_the_search_paths / puzzle_count}")
    print(f"\nTotal number of no solution = {total_number_of_no_solution}")
    print(f"Average number of no solution = {total_number_of_no_solution / puzzle_count}")
    print(f"\nTotal execution time = {total_execution_time} seconds")
    print(f"Average execution time = {total_execution_time / puzzle_count} seconds")
    if total_cost is not None:
        print(f"\nTotal cost = {total_cost}")
        print(f"Average cost = {total_cost / puzzle_count}")


if __name__ == "__main__":
    main()
