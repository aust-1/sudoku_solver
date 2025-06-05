"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import CompositeSolver
from sudoku.utils import SudokuPrinter


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board()
    puzzle = (
        "000005029"
        "000700000"
        "200001070"
        "000900000"
        "010607240"
        "083250001"
        "500062030"
        "000009086"
        "760008910"
    )
    board.load_from(puzzle)

    solver = CompositeSolver()
    solver.solve(board)

    SudokuPrinter.print(board)


if __name__ == "__main__":
    main()
