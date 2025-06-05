from __future__ import annotations

from sudoku.models import Board


class SudokuPrinter:
    """Simple ASCII printer for Sudoku boards."""

    @staticmethod
    def to_string(board: Board) -> str:
        """Return a multi-line string representation of ``board``.

        Args:
            board (Board): The Sudoku board to represent.

        Returns:
            str: A multi-line string representation of the board.
        """
        lines = []
        for i in range(3):
            for r in range(i * 3, (i + 1) * 3):
                row = ""
                for j in range(3):
                    row += (
                        " ".join(
                            str(board.get_cell(r, c)) for c in range(j * 3, (j + 1) * 3)
                        )
                        + " | "
                    )
                row = row[:-3]
                lines.append(row)
            lines.append("-" * 6 + "🞢" + "-" * 7 + "🞢" + "-" * 6)
        del lines[-1]
        return "\n".join(lines)

    @staticmethod
    def print(board: Board) -> None:
        """Print the Sudoku board to standard output.

        Args:
            board (Board): The Sudoku board to print.
        """
        print(SudokuPrinter.to_string(board))
