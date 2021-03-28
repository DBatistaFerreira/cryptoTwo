import copy
import time

from puzzle import Puzzle


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def get_next_states_from_possible_moves(puzzle):
    list_of_new_puzzle_states_from_possible_moves = []

    adjacent = puzzle.get_adjacent(row=puzzle.row, col=puzzle.col)

    for value in adjacent:
        row, col = puzzle.get_index_of(value)
        copy_of_puzzle = Puzzle(puzzle=copy.deepcopy(puzzle.s_puzzle))
        copy_of_puzzle.set_index(row, col)
        copy_of_puzzle.swap(value1=puzzle.get_value_at(puzzle.row, puzzle.col), value2=value)
        copy_of_puzzle.set_parent(puzzle)
        copy_of_puzzle.set_depth(puzzle.depth + 1)
        list_of_new_puzzle_states_from_possible_moves.append(copy_of_puzzle)

    return list_of_new_puzzle_states_from_possible_moves


class DepthFirst:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.graph = {}
        self.found = False
        self.visited = set()  # Set to keep track of visited nodes.
        self.solution = open("depth_first_solution_path.txt", "w")
        self.search = open("depth_first_search_path.txt", "w")

    def solve(self) -> bool:
        start_node = self.puzzle
        stack = Stack()
        stack.push(start_node)
        current = stack.pop()
        visited = set()
        search_path = [current]
        start_time = time.time()
        seconds = 60
        while not current.is_goal_state():
            temp = get_next_states_from_possible_moves(current)
            for item in temp:
                if item not in visited:
                    stack.push(item)
            visited.add(current)
            current = stack.pop()
            search_path.append(current)
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > seconds:
                print("No Solution, time exceeded 60 seconds")
                break
            # if current.depth > depth:
            #     break
        path = []
        while current is not None:
            path.append(current)
            current = current.parent

        for index, puzzle in enumerate(search_path):
            self.search.write(f"\n============================ Step {index} ============================\n")
            self.search.write(str(puzzle.s_puzzle))

        path.reverse()
        for index, puzzle in enumerate(path):
            self.solution.write(f"\n============================ Step {index} ============================\n")
            self.solution.write(str(puzzle.s_puzzle))

        self.close_files()

        return True

    def close_files(self) -> None:
        self.solution.close()
        self.search.close()
