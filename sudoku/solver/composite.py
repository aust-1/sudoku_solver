from __future__ import annotations

from typing import List

from sudoku.models import Board
from sudoku.solver.backtracking import BacktrackingSolver
from sudoku.solver.solver import Solver
from sudoku.solver.strategies import (
    ConstraintStrategy,
    EliminationStrategy,
    PairCandidateStrategy,
    PairChoiceStrategy,
    QuadCandidateStrategy,
    QuadChoiceStrategy,
    SingleCandidateStrategy,
    SingleChoiceStrategy,
    TripleCandidateStrategy,
    TripleChoiceStrategy,
)


class CompositeSolver(Solver):
    """Apply a sequence of logical strategies before backtracking."""

    def __init__(
        self,
        strategies: List[Solver] | None = None,
    ):
        """Initialise the composite solver with a list of strategies.

        Args:
            strategies (List[Solver] | None, optional): The list of strategies to apply. Defaults to None.
        """
        super().__init__()
        self.strategies = strategies or [
            EliminationStrategy(),
            SingleCandidateStrategy(),
            SingleChoiceStrategy(),
            PairChoiceStrategy(),
            PairCandidateStrategy(),
            TripleChoiceStrategy(),
            TripleCandidateStrategy(),
            QuadChoiceStrategy(),
            QuadCandidateStrategy(),
            ConstraintStrategy(),
        ]

    def apply(self, board: Board) -> bool:
        """Apply all strategies to the board until one succeeds.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if one of the strategies made a change to the board, `False` otherwise.
        """
        for strat in self.strategies:
            self.logger.info(f"Trying {strat.__class__.__name__}")
            if strat.apply(board):
                self.logger.info(
                    f"Strategy {strat.__class__.__name__} made a change to the board."
                )
                return True
        self.logger.info("No strategy made a change to the board.")
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
