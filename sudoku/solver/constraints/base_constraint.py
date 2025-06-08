from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class BaseConstraint(ABC):
    """A class representing a base constraint for the Sudoku board."""

    @abstractmethod
    def check(self, board: Board) -> bool:
        """Check if the constraint is satisfied on the given board.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool:
                ``True`` if the constraint is satisfied,
                ``False`` otherwise.
        """
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    @abstractmethod
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    @abstractmethod
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        return set()
