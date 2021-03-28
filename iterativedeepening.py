import time

from puzzle import get_next_states_from_possible_moves
from stack import Stack
from timerwrapper import exit_after
from pathlib import Path


class IterativeDeepening:
    def __init__(self, puzzle, puzzle_number):
        self.puzzle = puzzle
        self.graph = {}
        self.solved = False
        self.visited = set()  # Set to keep track of visited nodes.
        self.search_path = []
        self.solution_node = None
        Path(f"algorithm_outputs/itdeep/").mkdir(parents=True, exist_ok=True)
        self.solution = open(f"{puzzle_number}_id_solution_puzzle.txt", "w")
        self.search = open(f"{puzzle_number}_id_search_puzzle.txt", "w")

    def solve(self):
        def algorithm(depth):
            start_node = self.puzzle
            stack = Stack()
            stack.push(start_node)
            current = stack.pop()
            visited = set()
            self.search_path = [current]
            while not current.is_goal_state():
                if current.depth == depth:
                    temp = []
                else:
                    temp = get_next_states_from_possible_moves(current)
                for item in [node for node in temp if node not in visited]:
                    stack.push(item)
                visited.add(current)
                if not stack.is_empty():
                    current = stack.pop()
                else:
                    break
                self.search_path.append(current)

            self.solution_node = current
            return current.is_goal_state()

        @exit_after(60)
        def solve_with_timer():
            current_depth = 1
            found_goal_state = False
            while not found_goal_state:
                found_goal_state = algorithm(current_depth)
                current_depth += 1

        start_time = time.time()
        try:
            solve_with_timer()
            self.solved = True
        except KeyboardInterrupt:
            pass
        finally:
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(f"Final solve time: {int(elapsed_time)}")
            self.search.write(f"Final solve time: {int(elapsed_time)}")
            self.solution.write(f"Final solve time: {int(elapsed_time)}")

    def print_paths(self):
        if self.solved:
            path = []
            current = self.solution_node
            while current is not None:
                path.append(current)
                current = current.parent
            for index, puzzle in enumerate(self.search_path):
                self.search.write(f"\n============================ Step {index} ============================\n")
                self.search.write(str(puzzle.s_puzzle))

            path.reverse()
            for index, puzzle in enumerate(path):
                self.solution.write(f"\n============================ Step {index} ============================\n")
                self.solution.write(str(puzzle.s_puzzle))
        else:
            self.search.write(str(self.puzzle.s_puzzle))
            self.search.write("\nNo Solution")
            self.solution.write(str(self.puzzle.s_puzzle))
            self.solution.write("\nNo Solution")

        self.close_files()

    def close_files(self) -> None:
        self.solution.close()
        self.search.close()
