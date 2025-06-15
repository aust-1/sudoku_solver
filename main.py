"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import (
    BishopConstraint,
    CompositeSolver,
)
from sudoku.utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board(9)
    puzzle = (
        "800000000"
        "000001700"
        "000000000"
        "000000120"
        "000500008"
        "050000600"
        "070602030"
        "010300007"
        "000070090"
    )
    board.load_from(puzzle)
    board.add_constraints(
        BishopConstraint(
            {
                board.get_cell(0, 0),
                board.get_cell(1, 1),
                board.get_cell(2, 2),
                board.get_cell(3, 3),
                board.get_cell(4, 4),
                board.get_cell(5, 5),
                board.get_cell(6, 6),
                board.get_cell(7, 7),
                board.get_cell(8, 8),
            },
        ),
        BishopConstraint(
            {
                board.get_cell(0, 2),
                board.get_cell(1, 3),
                board.get_cell(2, 4),
                board.get_cell(3, 5),
                board.get_cell(4, 6),
                board.get_cell(5, 7),
                board.get_cell(6, 8),
            },
        ),
        BishopConstraint(
            {
                board.get_cell(0, 3),
                board.get_cell(1, 4),
                board.get_cell(2, 5),
                board.get_cell(3, 6),
                board.get_cell(4, 7),
                board.get_cell(5, 8),
            },
        ),
        BishopConstraint(
            {
                board.get_cell(2, 0),
                board.get_cell(3, 1),
                board.get_cell(4, 2),
                board.get_cell(5, 3),
                board.get_cell(6, 4),
                board.get_cell(7, 5),
                board.get_cell(8, 6),
            },
        ),
        BishopConstraint(
            {
                board.get_cell(3, 0),
                board.get_cell(4, 1),
                board.get_cell(5, 2),
                board.get_cell(6, 3),
                board.get_cell(7, 4),
                board.get_cell(8, 5),
            },
        ),
        BishopConstraint(
            {
                board.get_cell(4, 0),
                board.get_cell(3, 1),
                board.get_cell(2, 2),
                board.get_cell(1, 3),
                board.get_cell(0, 4),
            },
        ),
        BishopConstraint(
            {
                board.get_cell(5, 0),
                board.get_cell(4, 1),
                board.get_cell(3, 2),
                board.get_cell(2, 3),
                board.get_cell(1, 4),
                board.get_cell(0, 5),
            },
        ),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()
