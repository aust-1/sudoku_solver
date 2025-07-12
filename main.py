"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import CompositeSolver, PalindromeConstraint
from sudoku.utils import SudokuGUI


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
        PalindromeConstraint([
            board.get_cell(0, 1),
            board.get_cell(1, 1),
            board.get_cell(1, 2),
            board.get_cell(2, 2),
            board.get_cell(3, 2),
            board.get_cell(3, 1),
            board.get_cell(4, 1),
            board.get_cell(4, 0),
            board.get_cell(5, 0),
        ]),
        PalindromeConstraint([
            board.get_cell(0, 3),
            board.get_cell(0, 4),
            board.get_cell(1, 4),
            board.get_cell(1, 5),
            board.get_cell(2, 5),
            board.get_cell(2, 6),
            board.get_cell(2, 7),
            board.get_cell(1, 7),
            board.get_cell(1, 8),
        ]),
        PalindromeConstraint([
            board.get_cell(7, 0),
            board.get_cell(7, 1),
            board.get_cell(6, 1),
            board.get_cell(6, 2),
            board.get_cell(6, 3),
            board.get_cell(7, 3),
            board.get_cell(7, 4),
            board.get_cell(8, 4),
            board.get_cell(8, 5),
        ]),
        PalindromeConstraint([
            board.get_cell(3, 8),
            board.get_cell(4, 8),
            board.get_cell(4, 7),
            board.get_cell(5, 7),
            board.get_cell(5, 6),
            board.get_cell(6, 6),
            board.get_cell(7, 6),
            board.get_cell(7, 7),
            board.get_cell(8, 7),
        ]),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()

# TODO: implémenter uv
