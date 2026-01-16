from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class CoupleConstraint(BaseConstraint):
    """A class representing a Couple constraint."""

    def __init__(self, couple_cell1: Cell, couple_cell2: Cell, same: bool) -> None:
        """Initialize the Couple constraint.

        Args:
            couple_cell1 (Cell): The first cell to constrain.
            couple_cell2 (Cell): The second cell to constrain.
            same (bool): Whether the Couple constraint requires the cells to have
                the same parity or not.

        Raises:
            ValueError:
                If the cells are not adjacent.
        """
        super().__init__(ConstraintType.COUPLE)
        self.cell1 = couple_cell1
        self.cell2 = couple_cell2

        if (self.cell1.row - self.cell2.row) ** 2 + (
            self.cell1.col - self.cell2.col
        ) ** 2 != 1:
            msg = "Couple constraint cells must be adjacent."
            raise ValueError(msg)

        self.same = same

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> CoupleConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "couple", "cell1": "a1", "cell2": "a2", "same": true}

        Returns:
            CoupleConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cell1" not in data:
            msg = "Couple constraint requires 'cell1' field"
            raise ValueError(msg)
        if "cell2" not in data:
            msg = "Couple constraint requires 'cell2' field"
            raise ValueError(msg)
        if "same" not in data:
            msg = "Couple constraint requires 'same' field"
            raise ValueError(msg)

        cell1 = board.get_cell(pos=data["cell1"])
        cell2 = board.get_cell(pos=data["cell2"])

        return cls(cell1, cell2, data["same"])

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cell1": self.cell1.pos,
            "cell2": self.cell2.pos,
            "same": self.same,
        }

    @classmethod
    def same_parity(
        cls,
        couple_cell1: Cell,
        couple_cell2: Cell,
    ) -> CoupleConstraint:
        """Create a Couple constraint with tilde (same parity).

        Args:
            couple_cell1 (Cell): The first cell to constrain.
            couple_cell2 (Cell): The second cell to constrain.

        Returns:
            CoupleConstraint: The created Couple constraint.
        """
        return cls(couple_cell1, couple_cell2, same=True)

    @classmethod
    def different_parity(
        cls,
        couple_cell1: Cell,
        couple_cell2: Cell,
    ) -> CoupleConstraint:
        """Create a couple constraint with white dot.

        Args:
            couple_cell1 (Cell): The first cell to constrain.
            couple_cell2 (Cell): The second cell to constrain.

        Returns:
            CoupleConstraint: The created couple constraint.
        """
        return cls(couple_cell1, couple_cell2, same=False)

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the Ceuple constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]: A set of cells that do not satisfy the Couple constraint.
        """
        if (
            self.cell1.value is not None
            and self.cell2.value is not None
            and (self.cell1.value % 2 == self.cell2.value % 2) != self.same
        ):
            return {self.cell1, self.cell2}
        return set()

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the Couple constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        eliminated = False

        cell1_candidates: set[int] = set(self.cell1.candidates)
        cell2_candidates: set[int] = set(self.cell2.candidates)

        for v1 in cell1_candidates:
            possible = False
            for v2 in cell2_candidates:
                possible |= (v1 % 2 == v2 % 2) == self.same
            if not possible:
                eliminated |= self.cell1.eliminate_candidate(v1)

        for v2 in cell2_candidates:
            possible = False
            for v1 in cell1_candidates:
                possible |= (v1 % 2 == v2 % 2) == self.same
            if not possible:
                eliminated |= self.cell2.eliminate_candidate(v2)

        if eliminated:
            self._logger.debug(
                "Eliminated due to Couple "
                f"{'same_parity' if self.same else 'different_parity'}"
                f" in {self.cell1} and {self.cell2}",
            )
        return eliminated

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this Couple constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        # TODO: to implement, tilde (barée)

    @override
    def deep_copy(self) -> CoupleConstraint:
        """Create a deep copy of the constraint.

        Returns:
            CoupleConstraint: A deep copy of the constraint.
        """
        return CoupleConstraint(
            self.cell1,
            self.cell2,
            self.same,
        )

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        parity_str = "same_parity" if self.same else "different_parity"
        return f"CoupleConstraint([{self.cell1.pos}, {self.cell2.pos}], {parity_str})"


# TODO: implement logique si un nombre forcément entre deux tildes barrées
