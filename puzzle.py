import numpy as np


np.random.seed(0)


def format_puzzle(puzzle):
    str_builder = "("
    while puzzle:
        for i in range(3):
            if i == 0:
                str_builder += "("
            str_builder += str(puzzle[i])
            if i == 2:
                str_builder += ")"
            str_builder += ";"
        puzzle = puzzle[3:]

    str_builder = str_builder[:-1]
    str_builder += ")"

    return str_builder


def generate_puzzle():
    puzzle_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    puzzle = []
    while puzzle_values:
        random_index = np.random.randint(0, len(puzzle_values)) if len(puzzle_values) > 1 else 0
        puzzle.append(puzzle_values[random_index])
        del puzzle_values[random_index]

    return format_puzzle(puzzle)


def convert_puzzle_input(str_puzzle):
    puzzle = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    row = 0
    col = 0
    for char in str_puzzle:
        if char.isdigit():
            puzzle[row][col] = int(char)
            if col >= 2:
                row += 1
                col = 0
            else:
                col += 1

    return puzzle


class Puzzle:
    def __init__(self, puzzle=None):
        self.s_puzzle = np.array(puzzle)

    def set_puzzle(self, puzzle):
        self.s_puzzle = puzzle

    def get_puzzle(self):
        return self.s_puzzle

    def get_left(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return self.s_puzzle[row][col - 1] if col - 1 >= 0 else None
        except IndexError:
            return None

    def get_right(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return self.s_puzzle[row][col + 1] if col + 1 < len(self.s_puzzle[row]) else None
        except IndexError:
            return None

    def get_top(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return self.s_puzzle[row - 1][col] if row - 1 >= 0 else None
        except IndexError:
            return None

    def get_bottom(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return self.s_puzzle[row + 1][col] if row + 1 < len(self.s_puzzle) else None
        except IndexError:
            return None

    def get_left_index(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return (row, col - 1) if col - 1 < len(self.s_puzzle[row]) else None
        except IndexError:
            return None

    def get_right_index(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return (row, col + 1) if col + 1 < len(self.s_puzzle[row]) else None
        except IndexError:
            return None

    def get_top_index(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return (row - 1, col) if row - 1 < len(self.s_puzzle[row]) else None
        except IndexError:
            return None

    def get_bottom_index(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        try:
            return (row + 1, col) if row + 1 < len(self.s_puzzle[row]) else None
        except IndexError:
            return None

    def get_value_at(self, row, col):
        if row >= len(self.s_puzzle) or row < 0 or col >= len(self.s_puzzle[0]) or col < 0:
            raise IndexError(f"row or col index out of range {self.s_puzzle.shape}")
        return self.s_puzzle[row][col]

    def get_value_index(self, value):
        return np.where(self.s_puzzle == value)[0][0], np.where(self.s_puzzle == value)[1][0]
