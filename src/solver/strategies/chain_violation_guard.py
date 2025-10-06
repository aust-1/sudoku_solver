from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.solver import Solver

if TYPE_CHECKING:
    from models import Board, Cell


class ChainViolationGuardStrategy(Solver):
    """Eliminate candidates that lead to contradictions using backtracking."""

    @override
    def apply(self, board: Board) -> bool:
        """Try each candidate and remove those that lead to contradictions.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: ``True`` if any candidates were eliminated, ``False`` otherwise.
        """
        self._logger.debug("ChainViolationGuardStrategy running")
        moved = False
        for cell in board.get_all_cells():
            if cell.is_filled():
                continue
            for cand in set(cell.candidates):
                if not self._is_candidate_valid(board, cell, cand):
                    return cell.eliminate_candidate(cand)
        return moved

    @staticmethod
    def _is_candidate_valid(board: Board, cell: Cell, value: int) -> bool:
        """Check if placing ``value`` in ``cell`` can lead to a valid solution.

        Args:
            board (Board): The Sudoku board to test against.
            cell (Cell): The cell to try the value in.
            value (int): The value to test.

        Returns:
            bool: ``True`` if the resulting board can be solved, ``False`` otherwise.
        """
        from solver.composite import CompositeSolver
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

        copy = board.deep_copy()
        copy.get_cell(row=cell.row, col=cell.col).value = value
        solver = CompositeSolver(
            [
                EliminationStrategy(),
                HiddenSingleStrategy(),
                HiddenPairStrategy(),
                NakedPairStrategy(),
                HiddenTripleStrategy(),
                NakedTripleStrategy(),
                HiddenQuadStrategy(),
                NakedQuadStrategy(),
                XWingStrategy(),
                ConstraintStrategy(),
            ],
        )
        solved = solver.solve(copy)
        return solved or copy.is_valid()
