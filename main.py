"""Example script showcasing the Sudoku solver."""

from sudoku.models import Board
from sudoku.solver import CompositeSolver, PalindromeConstraint
from sudoku.utils import SudokuPrinter
from sudoku.utils import SudokuGUI


def main() -> None:
    """Load a puzzle, solve it and print the result."""
    board = Board()
    puzzle = (
        "100390000"
        "000002050"
        "020001000"
        "002600000"
        "000840025"
        "050030000"
        "000000009"
        "500070002"
        "600020508"
    )
    board.load_from(puzzle)
    board.add_constraint(
        PalindromeConstraint(
            [
                board.get_cell(8, 3),
                board.get_cell(8, 2),
                board.get_cell(7, 1),
                board.get_cell(6, 0),
                board.get_cell(5, 0),
                board.get_cell(4, 0),
                board.get_cell(3, 0),
                board.get_cell(2, 0),
                board.get_cell(1, 1),
                board.get_cell(0, 2),
                board.get_cell(0, 3),
                board.get_cell(0, 4),
                board.get_cell(0, 5),
                board.get_cell(1, 6),
                board.get_cell(2, 7),
                board.get_cell(3, 8),
                board.get_cell(4, 8),
                board.get_cell(5, 8),
                board.get_cell(6, 7),
                board.get_cell(7, 6),
                board.get_cell(7, 5),
                board.get_cell(6, 4),
                board.get_cell(5, 3),
                board.get_cell(4, 3),
                board.get_cell(3, 4),
                board.get_cell(4, 5),
            ]
        ),
    )

    solver = CompositeSolver()
    solver.solve(board)

    SudokuPrinter.print(board)
    cells = board.get_all_cells()
    for cell in cells:
        if cell.value is None:
            print(f"Cell at ({cell.row}, {cell.col}) is empty.")
            print("Candidates:", end=" ")
            print(", ".join(str(c) for c in sorted(cell.candidates)))

    try:
        gui = SudokuGUI(board)
        gui.run()
    except Exception as exc:  # GUI might fail in headless environments
        print(f"GUI could not be started: {exc}")


if __name__ == "__main__":
    main()
