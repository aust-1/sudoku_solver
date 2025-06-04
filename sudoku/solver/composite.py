from __future__ import annotations

from typing import List

from sudoku.model.board import Board

from .solver import Solver
from .single_candidate import SingleCandidateStrategy
from .only_choice import OnlyChoiceStrategy
from .elimination import EliminationStrategy
from .backtracking import BacktrackingSolver


class CompositeSolver(Solver):
    """Apply a sequence of logical strategies before backtracking."""

    def __init__(self, strategies: List[Solver] | None = None):
        """Initialise with a list of logical strategies."""
        self.strategies = strategies or [
            EliminationStrategy(),
            SingleCandidateStrategy(),
            OnlyChoiceStrategy(),
        ]

    def apply(self, board: Board) -> bool:
        """Apply strategies in order until one makes progress."""
        for strat in self.strategies:
            if strat.apply(board):
                return True
        return False

    def solve(self, board: Board) -> bool:
        """Solve ``board`` using strategies then backtracking."""
        progress = True
        while progress:
            progress = self.apply(board)
        bt = BacktrackingSolver()
        return bt.apply(board)
