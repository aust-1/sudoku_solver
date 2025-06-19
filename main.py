"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import (
    CompositeSolver,
    KillerConstraint,
    KropkiConstraint,
    PalindromeConstraint,
)
from sudoku.utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board(9)
    puzzle = (
        "000000000"
        "000000000"
        "000000000"
        "000000000"
        "000000000"
        "000000000"
        "000000000"
        "000000000"
        "000000000"
    )
    board.load_from(puzzle)
    board.add_constraints(
        KillerConstraint(
            {
                board.get_cell(0, 0),
                board.get_cell(1, 0),
                board.get_cell(1, 1),
                board.get_cell(2, 1),
            },
            28,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(0, 0),
                board.get_cell(1, 0),
                board.get_cell(1, 1),
                board.get_cell(2, 1),
            },
            28,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(0, 1),
                board.get_cell(0, 2),
                board.get_cell(0, 3),
                board.get_cell(1, 2),
            },
            15,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(0, 4),
                board.get_cell(0, 5),
                board.get_cell(0, 6),
            },
            13,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(0, 7),
                board.get_cell(0, 8),
            },
            16,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(1, 7),
                board.get_cell(1, 8),
                board.get_cell(2, 8),
            },
            8,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(2, 0),
                board.get_cell(3, 0),
                board.get_cell(4, 0),
                board.get_cell(5, 0),
            },
            20,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(2, 3),
                board.get_cell(2, 4),
                board.get_cell(3, 3),
            },
            10,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(2, 5),
                board.get_cell(3, 4),
                board.get_cell(3, 5),
            },
            16,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(3, 2),
                board.get_cell(4, 2),
            },
            10,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(3, 8),
                board.get_cell(4, 8),
                board.get_cell(5, 8),
                board.get_cell(6, 8),
            },
            27,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(4, 6),
                board.get_cell(5, 6),
            },
            9,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(5, 3),
                board.get_cell(6, 3),
                board.get_cell(6, 4),
            },
            17,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(5, 4),
                board.get_cell(5, 5),
                board.get_cell(6, 5),
            },
            13,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(6, 0),
                board.get_cell(7, 0),
                board.get_cell(7, 1),
            },
            7,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(6, 7),
                board.get_cell(7, 7),
                board.get_cell(7, 8),
                board.get_cell(8, 8),
            },
            18,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(7, 6),
                board.get_cell(8, 5),
                board.get_cell(8, 6),
                board.get_cell(8, 7),
            },
            18,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(8, 0),
                board.get_cell(8, 1),
            },
            16,
            board.size,
        ),
        KillerConstraint(
            {
                board.get_cell(8, 2),
                board.get_cell(8, 3),
                board.get_cell(8, 4),
            },
            14,
            board.size,
        ),
        KropkiConstraint.black({board.get_cell(0, 5), board.get_cell(0, 6)}),
        KropkiConstraint.black({board.get_cell(8, 2), board.get_cell(8, 3)}),
        KropkiConstraint.white({board.get_cell(1, 1), board.get_cell(2, 1)}),
        KropkiConstraint.white({board.get_cell(3, 3), board.get_cell(3, 4)}),
        KropkiConstraint.white({board.get_cell(3, 8), board.get_cell(4, 8)}),
        KropkiConstraint.white({board.get_cell(4, 0), board.get_cell(5, 0)}),
        KropkiConstraint.white({board.get_cell(5, 4), board.get_cell(5, 5)}),
        KropkiConstraint.white({board.get_cell(6, 7), board.get_cell(7, 7)}),
        PalindromeConstraint(
            [
                board.get_cell(7, 2),
                board.get_cell(6, 1),
                board.get_cell(5, 1),
                board.get_cell(4, 1),
                board.get_cell(3, 1),
                board.get_cell(2, 2),
                board.get_cell(1, 3),
                board.get_cell(1, 4),
                board.get_cell(1, 5),
                board.get_cell(2, 6),
                board.get_cell(3, 6),
                board.get_cell(4, 5),
                board.get_cell(4, 4),
            ],
        ),
        PalindromeConstraint(
            [
                board.get_cell(1, 6),
                board.get_cell(2, 7),
                board.get_cell(3, 7),
                board.get_cell(4, 7),
                board.get_cell(5, 7),
                board.get_cell(6, 6),
                board.get_cell(7, 5),
                board.get_cell(7, 4),
                board.get_cell(7, 3),
                board.get_cell(6, 2),
                board.get_cell(5, 2),
                board.get_cell(4, 3),
                board.get_cell(4, 4),
            ],
        ),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()
