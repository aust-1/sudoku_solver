"""Example script showcasing the Sudoku solver."""

from src.sudoku.models import Board
from src.sudoku.solver import CompositeSolver
from src.sudoku.solver.constraints import (
    BishopConstraint,
    KillerConstraint,
    KropkiConstraint,
    PalindromeConstraint,
    ParityConstraint,
)
from src.sudoku.utils import SudokuGUI


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
    board.load_from(puzzle)
    board.add_constraints(
        PalindromeConstraint(
            [
                board.get_cell(0, 1),
                board.get_cell(1, 1),
                board.get_cell(1, 2),
                board.get_cell(2, 2),
                board.get_cell(3, 2),
                board.get_cell(3, 1),
                board.get_cell(4, 1),
                board.get_cell(4, 0),
                board.get_cell(5, 0),
            ],
        ),
        KropkiConstraint.black(
            {
                board.get_cell(0, 0),
                board.get_cell(0, 1),
            },
        ),
        KillerConstraint(
            {
                board.get_cell(0, 0),
                board.get_cell(0, 1),
                board.get_cell(1, 0),
                board.get_cell(1, 1),
            },
            total_sum=20,
            board_size=9,
        ),
        ParityConstraint.odd(board.get_cell(4, 5)),
        ParityConstraint.even(board.get_cell(5, 5)),
        BishopConstraint(
            {
                board.get_cell(8, 8),
                board.get_cell(7, 7),
                board.get_cell(6, 6),
                board.get_cell(5, 5),
                board.get_cell(4, 4),
                board.get_cell(5, 3),
                board.get_cell(6, 2),
                board.get_cell(7, 1),
                board.get_cell(8, 0),
            },
        ),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()

# TODO: implémenter uv
