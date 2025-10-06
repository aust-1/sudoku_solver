"""Base constraint class for Sudoku variant constraints.

This module defines the abstract base class that all constraint implementations
must inherit from.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, override

from loggerplusplus import Logger

from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class BaseConstraint(ABC):
    """Abstract base class for Sudoku constraints.

    All constraint implementations must inherit from this class and implement
    the required abstract methods.
    """

    _msg: str = "Subclasses should implement this method."

    def __init__(
        self,
        constraint_type: ConstraintType | None = None,
        logger: Logger | None = None,
    ) -> None:
        """Initialize the base constraint.

        Args:
            constraint_type (ConstraintType | None):
                The type of the constraint. Defaults to None.
            logger (Logger | None):
                An optional logger instance for logging. Defaults to None.
        """
        self._logger = logger or Logger(
            identifier=self.__class__.__name__,
            follow_logger_manager_rules=True,
        )
        self.type: ConstraintType = constraint_type or ConstraintType.UNDEFINED

    @classmethod
    @abstractmethod
    def from_dict(cls, board: Board, data: dict[str, Any]) -> BaseConstraint:
        """Create a constraint instance from dictionary data.

        This is used for loading constraints from JSON configuration.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.

        Returns:
            BaseConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(BaseConstraint._msg)

    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        This is used for exporting constraints to JSON format.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
        }

    @abstractmethod
    def check(self, board: Board) -> set[Cell]:
        """Check if the constraint is satisfied on the given board.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]:
                A set of cells that do not satisfy the constraint.
                Empty if the constraint is satisfied.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(self._msg)

    @abstractmethod
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated, ``False`` otherwise.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(self._msg)

    def reachable_cells(  # noqa: PLR6301
        self,
        _board: Board,
        _cell: Cell,
    ) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            _board (Board): The Sudoku board.
            _cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        return set()

    def get_regions(self, _board: Board) -> dict[str, set[Cell]]:  # noqa: PLR6301
        """Get the regions defined by the constraint.

        Args:
            _board (Board): The Sudoku board.

        Returns:
            dict[str,set[Cell]]: A dictionary mapping region names to sets of cells.
        """
        return {}

    def draw(self, _gui: SudokuGUI) -> None:  # noqa: PLR6301
        """Draw this constraint on ``_gui`` if supported.

        Args:
            _gui (SudokuGUI): The GUI to draw on.
        """
        return

    @abstractmethod
    def deep_copy(self) -> BaseConstraint:
        """Create a deep copy of the constraint.

        Returns:
            BaseConstraint: A deep copy of the constraint.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(self._msg)

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        return f"{self.__class__.__name__}()"
