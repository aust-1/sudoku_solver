from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.solver import Solver

if TYPE_CHECKING:
    from models import Board


class BacktrackingSolver(Solver):
    """Recursive backtracking solver used as a last resort."""

    def __init__(self) -> None:
        """Initialise the backtracking solver and its helper strategies."""
        super().__init__()

        from solver.strategies import (
            ConstraintStrategy,
            EliminationStrategy,
            HiddenPairStrategy,
            HiddenQuadStrategy,
            HiddenSingleStrategy,
            HiddenTripleStrategy,
            NakedPairStrategy,
            NakedQuadStrategy,
            NakedTripleStrategy,
            XWingStrategy,
        )

        self.strategies: list[Solver] = [
            EliminationStrategy(),
            HiddenSingleStrategy(),
            NakedPairStrategy(),
            HiddenPairStrategy(),
            NakedTripleStrategy(),
            HiddenTripleStrategy(),
            NakedQuadStrategy(),
            HiddenQuadStrategy(),
            XWingStrategy(),
            ConstraintStrategy(),
        ]

    def _apply_strategies(self, board: Board) -> None:
        progress = True
        while progress:
            progress = False
            for strat in self.strategies:
                progress |= strat.apply(board)

    @override
    def apply(self, board: Board) -> bool:
        """Attempt to solve the Sudoku board using backtracking.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: ``True`` if the board is solved, ``False`` otherwise.

        """
        if not board.is_valid():
            return False

        self._apply_strategies(board)

        if not board.is_valid():
            return False
        if board.is_solved():
            return True

        unfilled = [cell for cell in board.get_all_cells() if not cell.is_filled()]
        unfilled.sort(key=lambda c: len(c.candidates))
        cell = unfilled[0]

        for cand in list(cell.candidates):
            self._logger.debug(
                f"Trying {cand} at ({cell.row}, {cell.col}) in backtracking",
            )
            copy = board.deep_copy()
            copy.get_cell(row=cell.row, col=cell.col).value = cand
            solver = BacktrackingSolver()
            if solver.apply(copy):
                board.copy_values_from(copy)
                self._logger.info(
                    f"Backtracking succeeded with {cand} at ({cell.row}, {cell.col})",
                )
                return True
        self._logger.info(f"Backtracking failed for cell ({cell.row}, {cell.col})")
        return False
