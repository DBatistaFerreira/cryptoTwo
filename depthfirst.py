# Using a Python dictionary to act as an adjacency list
import copy
from functools import lru_cache

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

class DepthFirst:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.graph = {}
        self.found = False
        self.visited = set()  # Set to keep track of visited nodes.
        # self.solution = open(depth_first_solution_path_output, "w")
        # self.search = open(depth_first_astar_search_path_output, "w")

    @lru_cache()
    def generate_graph(self, puzzle):
        self.graph[puzzle] = self.generate_all_states(puzzle)
        self.visited.add(puzzle)
        for puzzle in self.graph[puzzle]:
            if puzzle in self.visited:
                return
            else:
                if not self.found:
                    if puzzle.is_goal_state():
                        print("found")
                        self.found = True
                    else:
                        self.generate_graph(puzzle)
                else:
                    return

    @lru_cache()
    def generate_all_states(self, puzzle):

        set_of_possible_states = set()

        for row in range(3):
            for col in range(3):
                adjacent = puzzle.get_adjacent(row=row, col=col)

                for value in adjacent:
                    copy_of_puzzle = copy.deepcopy(puzzle)
                    copy_of_puzzle.swap(value1=puzzle.get_value_at(row=row, col=col), value2=value)
                    set_of_possible_states.add(copy_of_puzzle)
                    if copy_of_puzzle.is_goal_state():
                        print("found")
                        self.found = True

        return set_of_possible_states

    # def depth_first(visited, graph, node):
    #     if node not in visited:
    #         print(node)
    #         visited.add(node)
    #         for neighbour in graph[node]:
    #             depth_first(visited, graph, neighbour)
    #
