from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.backtracking import BacktrackingSolver
from solver.solver import Solver
from solver.strategies import (
    ChainViolationGuardStrategy,
    ConstraintStrategy,
    EliminationStrategy,
    HiddenPairStrategy,
    HiddenQuadStrategy,
    HiddenSingleStrategy,
    HiddenTripleStrategy,
    NakedPairStrategy,
    NakedQuadStrategy,
    NakedTripleStrategy,
    WWingStrategy,
    XWingStrategy,
)

if TYPE_CHECKING:
    from models import Board


class CompositeSolver(Solver):
    """Apply a sequence of logical strategies before backtracking."""

    def __init__(
        self,
        strategies: list[Solver] | None = None,
    ) -> None:
        """Initialise the composite solver with a list of strategies.

        Args:
            strategies (list[Solver] | None, optional):
                The list of strategies to apply. Defaults to None.

        """
        super().__init__()
        self.strategies = strategies or [
            EliminationStrategy(),
            HiddenSingleStrategy(),
            NakedPairStrategy(),
            HiddenPairStrategy(),
            ConstraintStrategy(),
            NakedTripleStrategy(),
            HiddenTripleStrategy(),
            NakedQuadStrategy(),
            HiddenQuadStrategy(),
            XWingStrategy(),
            WWingStrategy(),
            ChainViolationGuardStrategy(),
        ]

    @override
    def apply(self, board: Board) -> bool:
        """Apply all strategies to the board until one succeeds.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool:
                ``True`` if one of the strategies made a change to the board,
                ``False`` otherwise.

        """
        for strat in self.strategies:
            self.logger.info(f"Trying {strat.__class__.__name__}")
            if strat.apply(board):
                self.logger.info(
                    f"Strategy {strat.__class__.__name__} made a change to the board.",
                )
                return True
        self.logger.info("No strategy made a change to the board.")
        return False

    @override
    def solve(self, board: Board) -> bool:
        """Attempt to solve the Sudoku board using a combination of strategies.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: ``True`` if the board is solved, ``False`` otherwise.

        """
        progress = True
        while progress:
            progress = self.apply(board)
        bt = BacktrackingSolver()
        return bt.apply(board)
