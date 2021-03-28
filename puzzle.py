import copy
from math import sqrt
from numpy import array, zeros
import numpy as np
from cryptolib import range_inclusive


# np.random.seed(0)


def format_puzzle(puzzle) -> str:
    n = int(sqrt(len(puzzle)))
    str_builder = "("
    while puzzle:
        for i in range(n):
            if i == 0:
                str_builder += "("
            str_builder += str(puzzle[i])
            if i == n - 1:
                str_builder += ")"
            str_builder += ";"
        puzzle = puzzle[n:]

    str_builder = str_builder[:-1]
    str_builder += ")"

    return str_builder


def generate_puzzle(n) -> str:
    puzzle_values = list(range_inclusive(1, n**2))

    puzzle = []
    while puzzle_values:
        random_index = np.random.randint(0, len(puzzle_values)) if len(puzzle_values) > 1 else 0
        puzzle.append(puzzle_values[random_index])
        del puzzle_values[random_index]

    return format_puzzle(puzzle)


def convert_puzzle_input(str_puzzle) -> array:
    str_puzzle = str_puzzle.replace("(", "")
    str_puzzle = str_puzzle.replace(")", "")
    numbers = str_puzzle.split(";")
    n = int(sqrt(len(numbers)))
    puzzle = zeros((n, n), dtype=int)
    row = 0
    col = 0
    for number in numbers:
        puzzle[row][col] = int(number)
        if col >= n - 1:
            row += 1
            col = 0
        else:
            col += 1

    return puzzle


def build_goal_state(puzzle):
    goal_state = np.zeros(np.array(puzzle).shape, dtype=int)
    i = 1
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            goal_state[row][col] = i
            i += 1

    return goal_state


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


class Puzzle:
    def __init__(self, puzzle=None):
        self.parent = None
        self.depth = 0
        self.row = 0
        self.col = 0
        self.s_puzzle = np.array(puzzle)
        self.initial_state = np.array(puzzle)
        self.goal_state = build_goal_state(puzzle)

    def set_puzzle(self, puzzle):
        self.s_puzzle = puzzle

    def set_index(self, row, col):
        self.row = row
        self.col = col

    def set_parent(self, puzzle):
        self.parent = puzzle

    def set_depth(self, depth):
        self.depth = depth

    def get_puzzle(self):
        return self.s_puzzle

    def set_goal(self, goal):
        self.goal_state = goal

    def get_goal(self):
        return self.goal_state

    def get_left(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return self.s_puzzle[row][col - 1] if col - 1 >= 0 else None

    def get_right(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return self.s_puzzle[row][col + 1] if col + 1 < self.len_col() else None

    def get_top(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return self.s_puzzle[row - 1][col] if row - 1 >= 0 else None

    def get_bottom(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return self.s_puzzle[row + 1][col] if row + 1 < self.len_row() else None

    def get_left_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return (row, col - 1) if col - 1 >= 0 else None

    def get_right_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return (row, col + 1) if col + 1 < self.len_col() else None

    def get_top_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return (row - 1, col) if row - 1 >= 0 else None

    def get_bottom_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_row_of(value)
            col = self.get_col_of(value)

        return (row + 1, col) if row + 1 < self.len_row() else None

    def get_value_at(self, row, col):
        return None if row >= self.len_row() or row < 0 or col >= self.len_col() or col < 0 else self.s_puzzle[row][col]

    def get_index_of(self, value):
        return np.where(self.s_puzzle == value)[0][0], np.where(self.s_puzzle == value)[1][0]

    def get_row_of(self, value):
        return self.get_index_of(value)[0]

    def get_col_of(self, value):
        return self.get_index_of(value)[1]

    def get_n(self):
        return len(self.s_puzzle) * len(self.s_puzzle[0])

    def len_row(self):
        return len(self.s_puzzle)

    def len_col(self):
        return len(self.s_puzzle[0])

    def contains(self, value):
        return np.array(np.where(self.s_puzzle == value)).size > 0

    def valid_parameters(self, value=None, row=None, col=None):
        if value is not None and self.contains(value):
            return True
        elif row is not None and col is not None and self.is_valid_index(row, col):
            return True

        return False

    def is_valid_index(self, row, col):
        return row < self.len_row() or row >= 0 or col < self.len_col() or col >= 0

    def max_row_index(self):
        return self.len_row() - 1

    def max_col_index(self):
        return self.len_col() - 1

    def get_adjacent(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row, col = self.get_index_of(value)

        adjacent = []
        if self.get_left(row=row, col=col) is not None:
            adjacent.append(self.get_left(row=row, col=col))
        if self.get_right(row=row, col=col) is not None:
            adjacent.append(self.get_right(row=row, col=col))
        if self.get_top(row=row, col=col) is not None:
            adjacent.append(self.get_top(row=row, col=col))
        if self.get_bottom(row=row, col=col) is not None:
            adjacent.append(self.get_bottom(row=row, col=col))

        return np.array(adjacent)

    def is_adjacent(self, value1, value2):
        return value2 in self.get_adjacent(value1)

    def is_goal_state(self):
        is_correct = []
        for row in range(self.len_row()):
            for col in range(self.len_col()):
                if self.s_puzzle[row][col] == self.goal_state[row][col]:
                    is_correct.append(True)
                else:
                    is_correct.append(False)

        if is_correct.__contains__(False):
            return False

        return True

    def swap(self, value1, value2):
        if self.is_adjacent(value1, value2):
            row1, col1 = self.get_index_of(value1)
            row2, col2 = self.get_index_of(value2)
            self.s_puzzle[row2][col2] = value1
            self.s_puzzle[row1][col1] = value2
            return True

        return False

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Puzzle):
            return (self.s_puzzle == other.s_puzzle).all()
        return False

    def __hash__(self):
        return hash(str(self.s_puzzle))
