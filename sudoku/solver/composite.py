from __future__ import annotations

from typing import List

from sudoku.models.board import Board

from .solver import Solver
from .strategies.single_candidate import SingleCandidateStrategy
from .strategies.only_choice import OnlyChoiceStrategy
from .strategies.elimination import EliminationStrategy
from .backtracking import BacktrackingSolver


class CompositeSolver(Solver):
    """Apply a sequence of logical strategies before backtracking."""

    def __init__(self, strategies: List[Solver] | None = None):
        """Initialise the composite solver with a list of strategies.

        Args:
            strategies (List[Solver] | None, optional): The list of strategies to apply. Defaults to None.
        """
        self.strategies = strategies or [
            EliminationStrategy(),
            SingleCandidateStrategy(),
            OnlyChoiceStrategy(),
        ]

    def apply(self, board: Board) -> bool:
        """Apply all strategies to the board until one succeeds.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if one of the strategies made a change to the board, `False` otherwise.
        """
        for strat in self.strategies:
            if strat.apply(board):
                return True
        return False

    def solve(self, board: Board) -> bool:
        """Attempt to solve the Sudoku board using a combination of strategies and backtracking.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if the board is solved, `False` otherwise.
        """
        progress = True
        while progress:
            progress = self.apply(board)
        bt = BacktrackingSolver()
        return bt.apply(board)
