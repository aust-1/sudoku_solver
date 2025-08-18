from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from loggerplusplus import Logger

from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class BaseConstraint(ABC):
    """A class representing a base constraint for the Sudoku board.

    Attributes:
        _msg (str): A message indicating that subclasses should implement the methods.

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
        self.logger = logger or Logger(
            identifier=self.__class__.__name__,
            follow_logger_manager_rules=True,
        )
        self.type: ConstraintType = constraint_type or ConstraintType.UNDEFINED

    @abstractmethod
    def check(self, board: Board) -> bool:
        """Check if the constraint is satisfied on the given board.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool:
                ``True`` if the constraint is satisfied, ``False`` otherwise.

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
