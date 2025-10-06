"""Example script showcasing the Sudoku solver."""

import json

from models import Board
from solver import CompositeSolver
from solver.constraints import (
    PalindromeConstraint,
)
from utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    f = open("board.json")
    dico = json.load(f)
    board = Board.from_dict(dico)
    board.add_constraints(
        PalindromeConstraint(
            [
                board.get_cell(row=0, col=1),
                board.get_cell(row=1, col=1),
                board.get_cell(row=1, col=2),
                board.get_cell(row=2, col=2),
                board.get_cell(row=3, col=2),
                board.get_cell(row=3, col=1),
                board.get_cell(row=4, col=1),
                board.get_cell(row=4, col=0),
                board.get_cell(row=5, col=0),
            ],
        ),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()
