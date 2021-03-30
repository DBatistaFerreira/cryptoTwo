import time
from pathlib import Path

from puzzle import get_next_states_from_possible_moves
from stack import Stack
from timerwrapper import exit_after


class DepthFirst:
    def __init__(self, puzzle, puzzle_number):
        self.total_length_of_the_solution_path = 0
        self.total_length_of_the_search_path = 0
        self.execution_time = 0
        self.puzzle = puzzle
        self.graph = {}
        self.solved = False
        self.visited = set()  # Set to keep track of visited nodes.
        self.search_path = []
        self.solution_node = None
        output_dir = f"algorithm_outputs/df/"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.solution = open(f"{output_dir}{puzzle_number}_id_solution_puzzle.txt", "w")
        self.search = open(f"{output_dir}{puzzle_number}_id_search_puzzle.txt", "w")

    def solve(self):
        @exit_after(60)
        def algorithm(current_node):
            while not current_node.is_goal_state():
                children_nodes = get_next_states_from_possible_moves(current_node)
                for item in [node for node in children_nodes if node not in visited]:
                    stack.push(item)
                visited.add(current_node)
                current_node = stack.pop()
                self.search_path.append(current_node)

            self.solution_node = current_node

        visited = set()
        start_node = self.puzzle
        stack = Stack()
        stack.push(start_node)
        current = stack.pop()
        self.search_path = [current]
        start_time = time.time()
        try:
            algorithm(current)
            self.solved = True
        except KeyboardInterrupt:
            pass
        finally:
            current_time = time.time()
            elapsed_time = int(current_time - start_time)
            self.execution_time = elapsed_time
            print(f"Final solve time: {elapsed_time} seconds")
            self.search.write(f"Final solve time: {elapsed_time} seconds")
            self.solution.write(f"Final solve time: {elapsed_time} seconds")

    def print_paths(self):
        if self.solved:
            path = []
            current = self.solution_node
            while current is not None:
                path.append(current)
                current = current.parent

            self.total_length_of_the_search_path = len(self.search_path)
            for index, puzzle in enumerate(self.search_path):
                self.search.write(f"\n============================ Step {index} ============================\n")
                self.search.write(str(puzzle.s_puzzle))

            path.reverse()
            self.total_length_of_the_solution_path = len(path)
            for index, puzzle in enumerate(path):
                self.solution.write(f"\n============================ Step {index} ============================\n")
                self.solution.write(str(puzzle.s_puzzle))
        else:
            self.search.write(f"\n{str(self.puzzle.s_puzzle)}")
            self.search.write("\nNo Solution")
            self.solution.write(f"\n{str(self.puzzle.s_puzzle)}")
            self.solution.write("\nNo Solution")

        self.close_files()

    def close_files(self) -> None:
        self.solution.close()
        self.search.close()
