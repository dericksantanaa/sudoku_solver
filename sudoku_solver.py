"""9x9 sudoku solver

You can edit the puzzle below to try another board. 
Use 0 for Empty cells
"""

import matplotlib.pyplot as plt
import numpy as np


PUZZLE = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
])


def can_place(board, row, column, digit):
    if digit in board[row, :] or digit in board[:, column]:
        return False

    # Round down to the top-left corner of this cell's 3-by-3 box.
    box_top = (row // 3) * 3
    box_left = (column // 3) * 3
    box = board[box_top:box_top + 3, box_left:box_left + 3]
    return digit not in box


def backtrack(board):
    empty_cells = np.argwhere(board == 0)
    if empty_cells.size == 0:
        return True

    row, column = empty_cells[0]
    for digit in range(1, 10):
        if not can_place(board, row, column, digit):
            continue

        board[row, column] = digit
        if backtrack(board):
            return True

        # This guess led to a dead end. Erase it and try the next digit.
        board[row, column] = 0

    return False


def solve(puzzle):
    """Return one solution, None if impossible, or raise for invalid clues."""
    if puzzle.shape != (9, 9) or not np.issubdtype(puzzle.dtype, np.integer):
        raise ValueError("Enter a 9-by-9 grid of integers.")
    if np.any((puzzle < 0) | (puzzle > 9)):
        raise ValueError("Use digits 1–9 and 0 for empty cells.")

    board = puzzle.copy()
    for row, column in np.argwhere(puzzle != 0):
        digit = puzzle[row, column]
        # Temporarily hide this clue to check for duplicates elsewhere.
        board[row, column] = 0
        if not can_place(board, row, column, digit):
            raise ValueError(f"Conflicting clue at row {row + 1}, column {column + 1}.")
        board[row, column] = digit

    if backtrack(board):
        return board
    return None


def draw_board(ax, board, clues, title):
    ax.set_title(title)
    ax.set(xlim=(0, 9), ylim=(9, 0), aspect="equal")
    ax.set_axis_off()

    for line in range(10):
        width = 2 if line % 3 == 0 else 0.5
        ax.plot([line, line], [0, 9], color="#394a5c", linewidth=width, clip_on=False)
        ax.plot([0, 9], [line, line], color="#394a5c", linewidth=width, clip_on=False)

    for row, column in np.argwhere(board != 0):
        color = "#172534" if clues[row, column] else "#1763a6"
        ax.text(
            column + 0.5, row + 0.5, str(board[row, column]),
            ha="center", va="center", color=color, fontsize=13,
        )


def main():
    try:
        solution = solve(PUZZLE)
    except ValueError as error:
        print(error)
        return

    if solution is None:
        print("This puzzle has no solution.")
        return

    print(solution)
    clues = PUZZLE != 0
    figure, (puzzle_ax, solution_ax) = plt.subplots(1, 2, figsize=(9, 5), layout="constrained")
    figure.suptitle("Sudoku Solver", fontsize=18, fontweight="bold")
    draw_board(puzzle_ax, PUZZLE, clues, "Original puzzle")
    draw_board(solution_ax, solution, clues, "Solution")
    plt.show()


if __name__ == "__main__":
    main()
