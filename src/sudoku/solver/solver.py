from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from loggerplusplus import Logger  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from sudoku.models import Board


class Solver(ABC):
    """Base solver interface."""

    def __init__(self) -> None:
        """Initialize the solver."""
        self.logger = Logger(
            identifier=self.__class__.__name__,
            follow_logger_manager_rules=True,
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
        self.logger.info("Starting solve loop")
        while self.apply(board):
            self.logger.info("Board changed, continuing solve loop")
        self.logger.info("Solve loop finished")
        return board.is_solved()
