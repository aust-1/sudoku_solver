from __future__ import annotations

from abc import ABC, abstractmethod

from loggerplusplus import Logger

from sudoku.models import Board


class Solver(ABC):
    """Base solver interface."""

    def __init__(self):
        """Initialize the solver."""
        self.logger = Logger(
            identifier=self.__class__.__name__, follow_logger_manager_rules=True
        )

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
