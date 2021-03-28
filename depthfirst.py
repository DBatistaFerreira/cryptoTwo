import time

from puzzle import get_next_states_from_possible_moves
from stack import Stack
from timerwrapper import exit_after


class DepthFirst:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.graph = {}
        self.visited = set()  # Set to keep track of visited nodes.
        self.search_path = []
        self.solution_node = None
        self.solution = open("depth_first_solution_path.txt", "w")
        self.search = open("depth_first_search_path.txt", "w")

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
        except KeyboardInterrupt:
            pass
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f"Final solve time: {int(elapsed_time)}")

    def print_paths(self):
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

        self.close_files()

    def close_files(self) -> None:
        self.solution.close()
        self.search.close()
