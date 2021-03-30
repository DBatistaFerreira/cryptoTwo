import numpy as np
from sys import maxsize
from math import sqrt
from pathlib import Path
from timerwrapper import exit_after
from time import time
from cryptolib import range_inclusive


class AStar:
    def __init__(self, puzzle, puzzle_number):
        self.puzzle = puzzle
        self.closed = np.zeros((puzzle.len_row(), puzzle.len_col()), dtype=bool)
        self.solution = None
        self.search = None
        self.puzzle_number = puzzle_number
        self.total_swaps = 0
        self.total_cost = 0
        self.total_time = None

    def belongs_on_current_row(self, current):
        return self.belongs_on_row_index(current) == self.puzzle.get_row_of(current)

    def belongs_on_current_col(self, current):
        return self.belongs_on_col_index(current) == self.puzzle.get_col_of(current)

    def belongs_on_row_index(self, current):
        belongs_on_row = None
        for row in range(self.puzzle.len_row()):
            if current > row * sqrt(self.puzzle.get_n()):
                belongs_on_row = row

        return belongs_on_row

    def belongs_on_col_index(self, current):
        belongs_on_col = None
        for col in range(self.puzzle.len_col()):
            if current == self.belongs_on_row_index(current) * sqrt(self.puzzle.get_n()) + col + 1:
                belongs_on_col = col

        return belongs_on_col

    def swap_top_score_h1(self, current):
        top = self.puzzle.get_top(current)

        if self.closed[self.puzzle.get_row_of(top)][self.puzzle.get_col_of(top)]:
            return maxsize

        self.puzzle.swap(current, top)
        score = self.h1_score()
        self.puzzle.swap(current, top)

        return score

    def swap_left_score_h1(self, current):
        left = self.puzzle.get_left(current)
        if self.closed[self.puzzle.get_row_of(left)][self.puzzle.get_col_of(left)]:
            return maxsize
        self.puzzle.swap(current, left)
        score = self.h1_score()
        self.puzzle.swap(current, left)

        return score

    def swap_right_score_h1(self, current):
        right = self.puzzle.get_right(current)
        if self.closed[self.puzzle.get_row_of(right)][self.puzzle.get_col_of(right)]:
            return maxsize
        self.puzzle.swap(current, right)
        score = self.h1_score()
        self.puzzle.swap(current, right)

        return score

    def swap_bottom_score_h1(self, current):
        bottom = self.puzzle.get_bottom(current)
        if self.closed[self.puzzle.get_row_of(bottom)][self.puzzle.get_col_of(bottom)]:
            return maxsize
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

    def star_swap_h1(self, current):
        current_row, current_col = self.puzzle.get_index_of(current)
        self.search.write(f"Current state:\n{self.puzzle.s_puzzle}\n\n")
        if current == self.puzzle.goal_state[current_row][current_col]:
            self.closed[current_row][current_col] = True
            self.search.write(f"Current cell with value [{current}] has reached its goal position.\n")
            self.search.write(f"Cell [{current}] has been closed.\n\n")
        else:
            top, left, right, bottom = self.get_adjacent(current)
            swap_top_score, swap_left_score, swap_right_score, swap_bottom_score = self.get_swap_scores_h1(current)
            self.total_cost += min(swap_top_score, swap_left_score, swap_right_score, swap_bottom_score)
            self.total_swaps += 1
            self.solution.write(f"Current state:\n{self.puzzle.s_puzzle}\n\n")
            self.search.write(f"Swap scores with heuristic=1:\n")
            self.search.write(f"top:\t{swap_top_score}\n")
            self.search.write(f"left:\t{swap_left_score}\n")
            self.search.write(f"right:\t{swap_right_score}\n")
            self.search.write(f"bottom:\t{swap_bottom_score}\n\n")
            if swap_top_score <= swap_bottom_score:
                if swap_top_score <= swap_right_score and swap_top_score <= swap_left_score:
                    self.puzzle.swap(current, top)
                    self.search.write(f"top is chosen as the best swap option.\n")
                    self.search.write(f"Swapping current and top [{current}]<-->[{top}].\n\n")
                    self.solution.write(f"Swapping [{current}]<-->[{top}].\n\n")
                elif swap_right_score < swap_left_score:
                    self.puzzle.swap(current, right)
                    self.search.write(f"right is chosen as the best swap option.\n")
                    self.search.write(f"Swapping current and right [{current}]<-->[{right}].\n\n")
                    self.solution.write(f"Swapping [{current}]<-->[{right}].\n\n")
                elif swap_right_score == swap_left_score:
                    if self.belongs_on_current_row(current):
                        self.puzzle.swap(current, left)
                        self.search.write(f"left is chosen as the best swap option.\n")
                        self.search.write(f"Swapping current and left [{current}]<-->[{left}].\n\n")
                        self.solution.write(f"Swapping [{current}]<-->[{left}].\n\n")
                    else:
                        self.puzzle.swap(current, right)
                        self.search.write(f"right is chosen as the best swap option.\n")
                        self.search.write(f"Swapping current and right [{current}]<-->[{right}].\n\n")
                        self.solution.write(f"Swapping [{current}]<-->[{right}].\n\n")
                else:
                    self.puzzle.swap(current, left)
                    self.search.write(f"left is chosen as the best swap option.\n")
                    self.search.write(f"Swapping current and left [{current}]<-->[{left}].\n\n")
                    self.solution.write(f"Swapping [{current}]<-->[{left}].\n\n")
            else:
                if swap_bottom_score < swap_right_score and swap_bottom_score < swap_left_score:
                    self.puzzle.swap(current, bottom)
                    self.search.write(f"bottom is chosen as the best swap option.\n")
                    self.search.write(f"Swapping current and bottom [{current}]<-->[{bottom}].\n\n")
                    self.solution.write(f"Swapping [{current}]<-->[{bottom}].\n\n")
                elif swap_right_score < swap_left_score:
                    self.puzzle.swap(current, right)
                    self.search.write(f"right is chosen as the best swap option.\n")
                    self.search.write(f"Swapping current and bottom [{current}]<-->[{right}].\n\n")
                    self.solution.write(f"Swapping [{current}]<-->[{right}].\n\n")
                elif swap_right_score == swap_left_score:
                    if self.belongs_on_current_row(current):
                        self.puzzle.swap(current, left)
                        self.search.write(f"left is chosen as the best swap option.\n")
                        self.search.write(f"Swapping current and left [{current}]<-->[{left}].\n\n")
                        self.solution.write(f"Swapping [{current}]<-->[{left}].\n\n")
                    else:
                        self.puzzle.swap(current, right)
                        self.search.write(f"right is chosen as the best swap option.\n")
                        self.search.write(f"Swapping current and right [{current}]<-->[{right}].\n\n")
                        self.solution.write(f"Swapping [{current}]<-->[{right}].\n\n")
                else:
                    self.puzzle.swap(current, left)
                    self.search.write(f"left is chosen as the best swap option.\n")
                    self.search.write(f"Swapping current and left [{current}]<-->[{left}].\n\n")
                    self.solution.write(f"Swapping [{current}]<-->[{left}].\n\n")

    def star_swap_h2(self, current):
        current_row, current_col = self.puzzle.get_index_of(current)
        self.search.write(f"Current state:\n{self.puzzle.s_puzzle}\n\n")
        if self.belongs_on_current_row(current) and self.belongs_on_current_col(current):
            self.closed[current_row][current_col] = True
            self.search.write(f"Current cell with value [{current}] has reached its goal position.\n")
            self.search.write(f"Cell [{current}] has been closed.\n\n")
        else:
            top, left, right, bottom = self.get_adjacent(current)
            swap_top_score, swap_left_score, swap_right_score, swap_bottom_score = self.get_swap_scores_h2(current)
            self.total_cost += min(swap_top_score, swap_left_score, swap_right_score, swap_bottom_score)
            self.total_swaps += 1
            self.solution.write(f"Current state:\n{self.puzzle.s_puzzle}\n\n")
            self.search.write(f"Swap scores with heuristic=2:\n")
            self.search.write(f"top:\t{swap_top_score}\n")
            self.search.write(f"left:\t{swap_left_score}\n")
            self.search.write(f"right:\t{swap_right_score}\n")
            self.search.write(f"bottom:\t{swap_bottom_score}\n\n")
            if self.belongs_on_current_row(current):
                self.search.write(f"Current cell [{current}] belongs on current row.\n")
                if swap_left_score < swap_right_score:
                    self.puzzle.swap(current, left)
                    self.search.write(f"left is chosen as best swap option.\n")
                    self.search.write(f"Swapping current and left [{current}]<-->[{left}].\n\n")
                    self.solution.write(f"Swapping current and left [{current}]<-->[{left}].\n\n")
                else:
                    self.puzzle.swap(current, right)
                    self.search.write(f"right is chosen as best swap option.\n")
                    self.search.write(f"Swapping current and right [{current}]<-->[{right}].\n\n")
                    self.solution.write(f"Swapping current and right [{current}]<-->[{right}].\n\n")
            elif self.belongs_on_current_col(current):
                self.search.write(f"Current cell [{current}] belongs on current col.\n")
                if swap_top_score < swap_bottom_score:
                    self.puzzle.swap(current, top)
                    self.search.write(f"top is chosen as best swap option.\n")
                    self.search.write(f"Swapping current and top [{current}]<-->[{top}].\n\n")
                    self.solution.write(f"Swapping current and top [{current}]<-->[{top}].\n\n")
                else:
                    self.puzzle.swap(current, bottom)
                    self.search.write(f"bottom is chosen as best swap option.\n")
                    self.search.write(f"Swapping current and bottom [{current}]<-->[{bottom}].\n\n")
                    self.solution.write(f"Swapping current and bottom [{current}]<-->[{bottom}].\n\n")
            else:
                if swap_top_score < swap_bottom_score:
                    if swap_top_score <= swap_left_score and swap_top_score <= swap_right_score:
                        self.puzzle.swap(current, top)
                        self.search.write(f"top is chosen as best swap option.\n")
                        self.search.write(f"Swapping current and bottom [{current}]<-->[{top}].\n\n")
                        self.solution.write(f"Swapping current and bottom [{current}]<-->[{top}].\n\n")
                    elif swap_left_score < swap_right_score:
                        self.puzzle.swap(current, left)
                        self.search.write(f"left is chosen as best swap option.\n")
                        self.search.write(f"Swapping current and bottom [{current}]<-->[{left}].\n\n")
                        self.solution.write(f"Swapping current and bottom [{current}]<-->[{left}].\n\n")
                    else:
                        self.puzzle.swap(current, right)
                        self.search.write(f"right is chosen as best swap option.\n")
                        self.search.write(f"Swapping current and bottom [{current}]<-->[{right}].\n\n")
                        self.solution.write(f"Swapping current and bottom [{current}]<-->[{right}].\n\n")
                else:
                    self.puzzle.swap(current, right)
                    self.search.write(f"right is chosen as best swap option.\n")
                    self.search.write(f"Swapping current and bottom [{current}]<-->[{right}].\n\n")
                    self.solution.write(f"Swapping current and bottom [{current}]<-->[{right}].\n\n")

    def start(self, heuristic=2):
        if heuristic != 1 and heuristic != 2:
            print(f"Invalid heuristic [{heuristic}]. Heuristic can only be 1 or 2 [Default: heuristic=2].")
            return False

        output_dir = f"algorithm_outputs/astar/h{heuristic}/"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        astar_solution_file = f"{output_dir}{self.puzzle_number}_astar_solution_h{heuristic}.txt"
        astar_search_file = f"{output_dir}{self.puzzle_number}_astar_search_h{heuristic}.txt"

        self.solution = open(astar_solution_file, "w")
        self.search = open(astar_search_file, "w")

        self.search.write(f"=============================== SOLVE SEARCH START ===============================\n\n")
        self.solution.write(f"============================= SOLVE SOLUTION START =============================\n\n")
        self.search.write(f"Initial:\n{self.puzzle.initial_state}\n\n")
        self.search.write(f"Goal:\n{self.puzzle.goal_state}\n\n")
        self.solution.write(f"Initial:\n{self.puzzle.initial_state}\n\n")
        self.solution.write(f"Goal:\n{self.puzzle.goal_state}\n\n")
        self.solution.write(f"---------------------- Solution -----------------------\n\n")

        start_time = time()
        try:
            self.solve(heuristic)
        except KeyboardInterrupt:
            pass
        finally:
            end_time = time()
            self.total_time = end_time - start_time
            if self.puzzle.is_goal_state():
                self.write_stats(heuristic)
                return True

            self.no_solution(astar_solution_file, astar_search_file)

            return False

    def get_total_time(self):
        return "{:.4f}s".format(round(self.total_time, 4))

    def write_stats(self, heuristic):
        self.solution.write(f"----------------- Goal State Reached! -----------------\n\n")
        self.solution.write(f"Initial:\n{self.puzzle.initial_state}\n\n")
        self.solution.write(f"Current:\n{self.puzzle.s_puzzle}\n\n")
        self.solution.write(f"Goal:\n{self.puzzle.goal_state}\n\n")
        self.solution.write(f"A* algorithm with heuristic={heuristic} stats:\n")
        self.solution.write(f"Solved:\t{True}\n")
        self.solution.write(f"Time:\t{self.get_total_time()}\n")
        self.solution.write(f"Cost:\t{self.total_cost}\n")
        self.solution.write(f"Swaps:\t{self.total_swaps}\n\n")
        self.solution.write(f"============================== SOLVE SOLUTION END ==============================")
        self.search.write(f"----------------- Goal State Reached! -----------------\n\n")
        self.search.write(f"Initial:\n{self.puzzle.initial_state}\n\n")
        self.search.write(f"Current:\n{self.puzzle.s_puzzle}\n\n")
        self.search.write(f"Goal:\n{self.puzzle.goal_state}\n\n")
        self.search.write(f"A* algorithm with heuristic={heuristic} stats:\n")
        self.search.write(f"Solved:\t{True}\n")
        self.search.write(f"Time:\t{self.get_total_time()}\n")
        self.search.write(f"Cost:\t{self.total_cost}\n")
        self.search.write(f"Swaps:\t{self.total_swaps}\n\n")
        self.search.write(f"================================ SOLVE SEARCH END ================================")
        self.close_files()

    def no_solution(self, astar_solution_path, astar_search_path):
        self.solution.close()
        self.search.close()
        self.solution = open(astar_solution_path, "w")
        self.search = open(astar_search_path, "w")
        self.solution.write("no solution")
        self.search.write("no solution")
        self.close_files()

    @exit_after(60)
    def solve(self, heuristic):
        for current in range_inclusive(1, self.puzzle.get_n()):
            self.search.write(f"---------------- Evaluating cell with value: [{current}] ----------------\n\n")
            while not self.closed[self.belongs_on_row_index(current)][self.belongs_on_col_index(current)]:
                if heuristic == 1:
                    self.star_swap_h1(current)
                else:
                    self.star_swap_h2(current)

            self.search.write(f"----------------- Closing cell with value: [{current}] ------------------\n\n")

        self.solution.write(f"Current:\n{self.puzzle.s_puzzle}\n\n")

    def close_files(self):
        self.solution.close()
        self.search.close()
