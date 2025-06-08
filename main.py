"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import (
    CompositeSolver,
    KingConstraint,
    KnightConstraint,
)
from sudoku.utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board(9)
    puzzle = (
        "900000006"
        "000000000"
        "000000000"
        "000302000"
        "000000000"
        "000801000"
        "000000000"
        "000000000"
        "503000709"
    )
    board.load_from(puzzle)
    board.add_constraints(KingConstraint(), KnightConstraint())

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()
