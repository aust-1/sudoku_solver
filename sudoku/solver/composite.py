from __future__ import annotations

from typing import List

from sudoku.model.board import Board

from .solver import Solver
from .single_candidate import SingleCandidateStrategy
from .only_choice import OnlyChoiceStrategy
from .elimination import EliminationStrategy
from .backtracking import BacktrackingSolver


class CompositeSolver(Solver):
    def __init__(self, strategies: List[Solver] | None = None):
        self.strategies = strategies or [
            EliminationStrategy(),
            SingleCandidateStrategy(),
            OnlyChoiceStrategy(),
        ]

    def apply(self, board: Board) -> bool:
        for strat in self.strategies:
            if strat.apply(board):
                return True
        return False

    def solve(self, board: Board) -> bool:
        progress = True
        while progress:
            progress = self.apply(board)
        bt = BacktrackingSolver()
        return bt.apply(board)
