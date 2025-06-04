from __future__ import annotations

from abc import ABC, abstractmethod

from sudoku.model.board import Board


class Solver(ABC):
    """Base solver interface."""

    @abstractmethod
    def apply(self, board: Board) -> bool:
        """Apply a solving step. Returns True if board changed."""

    def solve(self, board: Board) -> bool:
        while self.apply(board):
            pass
        return board.is_solved()
