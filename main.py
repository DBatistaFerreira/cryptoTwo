import puzzle as p
import astar as a
import numpy as np


def main():
    s_puzzle = p.generate_puzzle()
    print("s_puzzle: ", s_puzzle)

    s_puzzle = p.convert_puzzle_input(s_puzzle)
    print("s_puzzle: ", s_puzzle)

    test(s_puzzle)


def test(s_puzzle):
    puzzle = p.Puzzle(s_puzzle)
    star = a.AStar(puzzle)
    print(f"current: \n{star.puzzle.s_puzzle}")
    print(f"goal: \n{star.puzzle.goal_state}")
    solved = star.solve()
    print("==== SOLVED ====")
    print(f"current: \n{star.puzzle.s_puzzle}")
    print(f"goal: \n{star.puzzle.goal_state}")
    print(f"solved: {solved}")

    # print(f"h2_score: {star.h1_score()}")
    # top, left, right = 3, 1, 2
    # if top <= left and top <= right:
    #     print("obvs yes")
    # else:
    #     print("obvs no")
    # if top <= (left or right):
    #     print(f"{top} <= ({left} and {right})\nAMAZING!")
    # else:
    #     print(f"nope")


if __name__ == "__main__":
    main()
