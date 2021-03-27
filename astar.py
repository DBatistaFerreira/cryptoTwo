import numpy as np
from sys import maxsize
from math import sqrt


astar_solution_path_output = "astar_solution_path_output.txt"
astar_search_path_output = "astar_search_path_output.txt"


def range_inclusive(start, end):
    return range(start, end + 1)


class AStar:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.closed = np.zeros((puzzle.len_row(), puzzle.len_col()), dtype=bool)
        self.solution = open(astar_solution_path_output, "w")
        self.search = open(astar_search_path_output, "w")

    # number of misplaced tiles from current state to goal state
    # NOT USED
    def misplaced_score(self):
        misplaced = 0
        for row in range(self.puzzle.len_row()):
            for col in range(self.puzzle.len_col()):
                if self.puzzle.s_puzzle[row][col] != self.puzzle.goal_state[row][col]:
                    misplaced += 1

        return misplaced

    def belongs_on_current_row(self, current):
        return self.belongs_on_row_index(current) == self.puzzle.get_row_of(current)

    def belongs_on_row_index(self, current):
        belongs_on_row = None
        for row in range(self.puzzle.len_row()):
            if current > row * sqrt(self.puzzle.get_n()):
                belongs_on_row = row

        return belongs_on_row

    def belongs_on_current_col(self, current):
        return self.belongs_on_col_index(current) == self.puzzle.get_col_of(current)

    def belongs_on_col_index(self, current):
        belongs_on_col = None
        for col in range(self.puzzle.len_col()):
            if current == self.belongs_on_row_index(current) * sqrt(self.puzzle.get_n()) + col + 1:
                belongs_on_col = col

        return belongs_on_col

    def swap_top_score_h1(self, current):
        top = self.puzzle.get_top(current)
        self.puzzle.swap(current, top)
        score = self.h1_score()
        self.puzzle.swap(current, top)

        return score

    def swap_left_score_h1(self, current):
        left = self.puzzle.get_left(current)
        self.puzzle.swap(current, left)
        score = self.h1_score()
        self.puzzle.swap(current, left)

        return score

    def swap_right_score_h1(self, current):
        right = self.puzzle.get_right(current)
        self.puzzle.swap(current, right)
        score = self.h1_score()
        self.puzzle.swap(current, right)

        return score

    def swap_bottom_score_h1(self, current):
        bottom = self.puzzle.get_bottom(current)
        self.puzzle.swap(current, bottom)
        score = self.h1_score()
        self.puzzle.swap(current, bottom)

        return score

    def swap_top_score_h2(self, current):
        top = self.puzzle.get_top(current)
        if self.closed[self.puzzle.get_row_of(top)][self.puzzle.get_col_of(top)]:
            return maxsize
        return abs(self.belongs_on_row_index(current) - self.puzzle.get_row_of(self.puzzle.get_top(current)))

    def swap_bottom_score_h2(self, current):
        bottom = self.puzzle.get_bottom(current)
        if self.closed[self.puzzle.get_row_of(bottom)][self.puzzle.get_col_of(bottom)]:
            return maxsize
        return abs(self.belongs_on_row_index(current) - self.puzzle.get_row_of(self.puzzle.get_bottom(current)))

    def swap_left_score_h2(self, current):
        left = self.puzzle.get_left(current)
        if self.closed[self.puzzle.get_row_of(left)][self.puzzle.get_col_of(left)]:
            return maxsize
        return abs(self.belongs_on_col_index(current) - self.puzzle.get_col_of(self.puzzle.get_left(current)))

    def swap_right_score_h2(self, current):
        right = self.puzzle.get_right(current)
        if self.closed[self.puzzle.get_row_of(right)][self.puzzle.get_col_of(right)]:
            return maxsize
        return abs(self.belongs_on_col_index(current) - self.puzzle.get_col_of(self.puzzle.get_right(current)))

    # def f_score(self):
    #     return self.misplaced_score() + self.row_score()

    def h_score(self):
        return 0

    # def start_index(self):
    #     return int(floor(self.puzzle.len_row() / 2)), int(floor(self.puzzle.len_col() / 2))

    def get_adjacent(self, current):
        """
        Get the adjacent elements in the s_puzzle from the current position's value.
        Returns in order top, left, right, bottom.

        :param current: current position's value
        :return: top, left, right, bottom
        """
        top = self.puzzle.get_top(current)
        left = self.puzzle.get_left(current)
        right = self.puzzle.get_right(current)
        bottom = self.puzzle.get_bottom(current)

        return top, left, right, bottom

    def get_swap_scores_h1(self, current):
        swap_top_score = maxsize if self.puzzle.get_top(current) is None else self.swap_top_score_h1(current)
        swap_left_score = maxsize if self.puzzle.get_left(current) is None else self.swap_left_score_h1(current)
        swap_right_score = maxsize if self.puzzle.get_right(current) is None else self.swap_right_score_h1(current)
        swap_bottom_score = maxsize if self.puzzle.get_bottom(current) is None else self.swap_bottom_score_h1(current)

        return swap_top_score, swap_left_score, swap_right_score, swap_bottom_score

    def get_swap_scores_h2(self, current):
        """
        Get the swap scores of the s_puzzle's current position's value.
        Returns in order top, left, right, bottom
        :param current: current position's value
        :return: swap_top_score, swap_left_score, swap_right_score, swap_bottom_score
        """
        swap_top_score = maxsize if self.puzzle.get_top(current) is None else self.swap_top_score_h2(current)
        swap_left_score = maxsize if self.puzzle.get_left(current) is None else self.swap_left_score_h2(current)
        swap_right_score = maxsize if self.puzzle.get_right(current) is None else self.swap_right_score_h2(current)
        swap_bottom_score = maxsize if self.puzzle.get_bottom(current) is None else self.swap_bottom_score_h2(current)

        return swap_top_score, swap_left_score, swap_right_score, swap_bottom_score

    def manhattan_distance(self, current):
        return abs(self.belongs_on_row_index(current) - self.puzzle.get_row_of(current)) + abs(
            self.belongs_on_col_index(current) - self.puzzle.get_col_of(current))

    def h1_score(self):
        score = 0
        for current in range_inclusive(1, self.puzzle.get_n()):
            score += self.manhattan_distance(current)

        return score

    # NOT USED
    def get_swap_row_scores(self, current):
        """
        Get the swap top and bottoms scores of the s_puzzle's current position's value.
        Returns in order swap_top_score, swap_bottom_score
        :param current: current position's value
        :return: swap_top_score, swap_bottom_score
        """
        swap_top_score = maxsize if self.puzzle.get_top(current) is None else self.swap_top_score_h2(current)
        swap_bottom_score = maxsize if self.puzzle.get_bottom(current) is None else self.swap_bottom_score_h2(current)

        return swap_top_score, swap_bottom_score

    # NOT USED
    def get_swap_col_scores(self, current):
        """
        Get the swap left and right scores of the s_puzzle's current position's value.
        Returns in order swap_left_score, swap_right_score
        :param current: current position's value
        :return: swap_left_score, swap_right_score
        """
        swap_left_score = maxsize if self.puzzle.get_left(current) is None else self.swap_left_score_h2(current)
        swap_right_score = maxsize if self.puzzle.get_right(current) is None else self.swap_right_score_h2(current)

        return swap_left_score, swap_right_score

    def reached_goal_state(self):
        is_correct = []
        for current in range_inclusive(1, self.puzzle.get_n()):
            if current != self.puzzle.s_puzzle[self.belongs_on_row_index(current)][self.belongs_on_col_index(current)]:
                is_correct.append(False)
            else:
                is_correct.append(True)

        if is_correct.__contains__(False):
            return False

        return True

    def star_swap_h1(self, current):
        top, left, right, bottom = self.get_adjacent(current)
        current_row, current_col = self.puzzle.get_index_of(current)
        swap_top_score, swap_left_score, swap_right_score, swap_bottom_score = self.get_swap_scores_h1(current)
        if current == self.puzzle.goal_state[current_row][current_col]:
            self.closed[current_row][current_col] = True
        elif swap_top_score < (swap_left_score or swap_right_score or swap_bottom_score):
            self.puzzle.swap(current, top)

    def star_swap_h2(self, current):
        top, left, right, bottom = self.get_adjacent(current)
        current_row, current_col = self.puzzle.get_index_of(current)
        swap_top_score, swap_left_score, swap_right_score, swap_bottom_score = self.get_swap_scores_h2(current)
        if self.belongs_on_current_row(current) and self.belongs_on_current_col(current):
            self.closed[current_row][current_col] = True
        elif self.belongs_on_current_row(current):
            if swap_left_score < swap_right_score:
                self.puzzle.swap(current, left)
            else:
                self.puzzle.swap(current, right)
        elif self.belongs_on_current_col(current):
            if swap_top_score < swap_bottom_score:
                self.puzzle.swap(current, top)
            else:
                self.puzzle.swap(current, bottom)
        else:
            if swap_top_score <= swap_bottom_score:
                if swap_top_score <= (swap_left_score and swap_right_score):
                    self.puzzle.swap(current, top)
                elif swap_left_score < swap_right_score:
                    self.puzzle.swap(current, left)
                else:
                    self.puzzle.swap(current, right)
            else:
                if swap_bottom_score <= (swap_left_score and swap_right_score):
                    self.puzzle.swap(current, bottom)
                elif swap_left_score <= swap_right_score:
                    self.puzzle.swap(current, left)
                else:
                    self.puzzle.swap(current, right)

    def solve(self):
        if self.reached_goal_state():
            self.solution.write("Already in goal state.")
            self.search.write("Already in goal state.")
            self.close_files()
            return True

        for current in range_inclusive(1, self.puzzle.get_n()):
            print(f"\n===========\ncurrent: \n{self.puzzle.s_puzzle}\nclosed: \n{self.closed}\n============")
            while not self.closed[self.belongs_on_row_index(current)][self.belongs_on_col_index(current)]:
                self.star_swap_h2(current)

        self.close_files()

        if not self.reached_goal_state():
            self.no_solution()
            return False
        # elif time to solve longer than 60 seconds no solution

        return True

    def no_solution(self):
        self.solution = open(astar_solution_path_output, "w")
        self.search = open(astar_search_path_output, "w")
        self.solution.write("no solution")
        self.search.write("no solution")
        self.close_files()

    def close_files(self):
        self.solution.close()
        self.search.close()
