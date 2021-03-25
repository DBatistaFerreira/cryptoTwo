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

    def get_left(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return self.s_puzzle[row][col - 1] if col - 1 >= 0 else None

    def get_right(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return self.s_puzzle[row][col + 1] if col + 1 < self.len_col() else None

    def get_top(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return self.s_puzzle[row - 1][col] if row - 1 >= 0 else None

    def get_bottom(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return self.s_puzzle[row + 1][col] if row + 1 < self.len_row() else None

    def get_left_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return (row, col - 1) if col - 1 >= 0 else None

    def get_right_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return (row, col + 1) if col + 1 < self.len_col() else None

    def get_top_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return (row - 1, col) if row - 1 >= 0 else None

    def get_bottom_index(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row = self.get_value_row(value)
            col = self.get_value_col(value)

        return (row + 1, col) if row + 1 < self.len_row() else None

    def get_value_at(self, row, col):
        return None if row >= self.len_row() or row < 0 or col >= self.len_col() or col < 0 else self.s_puzzle[row][col]

    def get_value_index(self, value):
        return np.where(self.s_puzzle == value)[0][0], np.where(self.s_puzzle == value)[1][0]

    def get_value_row(self, value):
        return self.get_value_index(value)[0]

    def get_value_col(self, value):
        return self.get_value_index(value)[1]

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

    def get_adjacent(self, value=None, row=None, col=None):
        if not self.valid_parameters(value, row, col):
            return None

        if value is not None:
            row, col = self.get_value_index(value)

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

    def swap(self, value1, value2):
        if self.is_adjacent(value1, value2):
            self.s_puzzle[self.get_value_row(value2)][self.get_value_col(value2)] = value1
            self.s_puzzle[self.get_value_row(value1)][self.get_value_col(value1)] = value2
            return True

        return False
