"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import CompositeSolver, KnightConstraint, UniversalConstraint
from sudoku.utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board(9)
    puzzle = (
        "000020010"
        "060000000"
        "000000000"
        "000090080"
        "100000000"
        "007000000"
        "500000008"
        "000000900"
        "070300000"
    )
    board.load_from(puzzle)
    board.add_constraints(
        KnightConstraint(),
        UniversalConstraint(),
    )

    solver = CompositeSolver()

    gui = SudokuGUI(board)
    gui.run_stepwise(solver)


if __name__ == "__main__":
    main()
