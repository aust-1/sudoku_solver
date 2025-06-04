from __future__ import annotations

from sudoku.model.board import Board


class SudokuPrinter:
    @staticmethod
    def to_string(board: Board) -> str:
        lines = []
        for r in range(9):
            row = ' '.join(str(board.get_cell(r, c)) for c in range(9))
            lines.append(row)
        return '\n'.join(lines)

    @staticmethod
    def print(board: Board) -> None:
        print(SudokuPrinter.to_string(board))
