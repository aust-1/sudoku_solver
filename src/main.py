"""Example script showcasing the Sudoku solver."""

from models import Board
from solver import CompositeSolver
from solver.constraints import (
    PalindromeConstraint,
)
from utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board(9)
    puzzle = (
        "006005420"
        "502400000"
        "000020005"
        "000900030"
        "020040000"
        "007000004"
        "200009041"
        "409001002"
        "010204309"
    )
    board.load_from_string(puzzle)
    board.add_constraints(
        PalindromeConstraint(
            [
                board.get_cell(r=0, c=1),
                board.get_cell(r=1, c=1),
                board.get_cell(r=1, c=2),
                board.get_cell(r=2, c=2),
                board.get_cell(r=3, c=2),
                board.get_cell(r=3, c=1),
                board.get_cell(r=4, c=1),
                board.get_cell(r=4, c=0),
                board.get_cell(r=5, c=0),
            ],
        ),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()
