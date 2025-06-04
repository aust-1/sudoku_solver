from __future__ import annotations

"""Utility functions for pretty-printing Sudoku boards."""

from sudoku.model.board import Board


class SudokuPrinter:
    """Simple ASCII printer for Sudoku boards."""

    @staticmethod
    def to_string(board: Board) -> str:
        """Return a multi-line string representation of ``board``."""
        lines = []
        for r in range(9):
            row = " ".join(str(board.get_cell(r, c)) for c in range(9))
            lines.append(row)
        return "\n".join(lines)

    @staticmethod
    def print(board: Board) -> None:
        """Print ``board`` to standard output."""
        print(SudokuPrinter.to_string(board))
