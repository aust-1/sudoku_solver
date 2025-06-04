from __future__ import annotations

"""Input/output helpers for Sudoku boards."""


class SudokuIO:
    """Read or write puzzles from files."""

    @staticmethod
    def read_from_file(path: str) -> str:
        """Return the file contents located at ``path``."""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_to_file(path: str, content: str) -> None:
        """Write ``content`` to ``path``."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
