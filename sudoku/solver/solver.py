from __future__ import annotations

from abc import ABC, abstractmethod

from sudoku.model.board import Board


class Solver(ABC):
    """Base solver interface."""

    @abstractmethod
    def apply(self, board: Board) -> bool:
        """Apply a solving step.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if the board was modified, `False` otherwise.
        """

    def solve(self, board: Board) -> bool:
        """Attempt to solve the Sudoku board until no more changes can be made.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if the board is solved, `False` otherwise.
        """
        while self.apply(board):
            pass
        return board.is_solved()
