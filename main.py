from sudoku.model import Board
from sudoku.solver import CompositeSolver
from sudoku.util import SudokuPrinter


def main():
    board = Board()
    # Example puzzle (0 for empty cells)
    puzzle = (
        "530070000"
        "600195000"
        "098000060"
        "800060003"
        "400803001"
        "700020006"
        "060000280"
        "000419005"
        "000080079"
    )
    board.load_from(puzzle)

    solver = CompositeSolver()
    solver.solve(board)

    SudokuPrinter.print(board)


if __name__ == "__main__":
    main()
