from __future__ import annotations

"""Input/output helpers for Sudoku boards."""


class SudokuIO:
    """Read or write puzzles from files."""

    @staticmethod
    def read_from_file(path: str) -> str:
        """Read the contents of a file.

        Args:
            path (str): The path to the file.

        Returns:
            str: The contents of the file.
        """
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_to_file(path: str, content: str) -> None:
        """Write the contents to a file.

        Args:
            path (str): The path to the file.
            content (str): The contents to write to the file.
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
