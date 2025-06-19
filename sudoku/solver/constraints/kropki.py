from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.utils.gui import SudokuGUI


class KropkiConstraint(BaseConstraint):
    """A class representing a Kropki constraint."""

    def __init__(self, kropki_cells: set[Cell], color: str) -> None:
        """Initialize the Kropki constraint.

        Args:
            kropki_cells (set[Cell]): The cells to constrain.
            color (str): The color of the Kropki constraint (black or white).

        Raises:
            ValueError: If the cells are not adjacent.
            ValueError: If the color is not 'black' or 'white'.
        """
        super().__init__()
        self.cell1, self.cell2 = kropki_cells

        if (abs(self.cell1.row - self.cell2.row) == 1) == (
            abs(self.cell1.col - self.cell2.col) == 1
        ):
            msg = "Kropki constraint cells must be adjacent."
            raise ValueError(msg)

        if color == "black":
            self.is_black_dot = True
            self.cell1.eliminate(5)
            self.cell2.eliminate(5)
            self.cell1.eliminate(7)
            self.cell2.eliminate(7)
            self.cell1.eliminate(9)
            self.cell2.eliminate(9)
        elif color == "white":
            self.is_black_dot = False
        else:
            msg = f"Invalid Kropki constraint color: {color}. Use 'black' or 'white'."
            raise ValueError(msg)

    @classmethod
    def black(cls, kropki_cells: set[Cell]) -> KropkiConstraint:
        """Create a Kropki constraint with black dot.

        Args:
            kropki_cells (set[Cell]): The cells to constrain.

        Returns:
            KropkiConstraint: The created Kropki constraint.
        """
        return cls(kropki_cells, color="black")

    @classmethod
    def white(cls, kropki_cells: set[Cell]) -> KropkiConstraint:
        """Create a Kropki constraint with white dot.

        Args:
            kropki_cells (set[Cell]): The cells to constrain.

        Returns:
            KropkiConstraint: The created Kropki constraint.
        """
        return cls(kropki_cells, color="white")

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the Kropki constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: `True` if the Kropki constraint is satisfied, `False` otherwise.
        """
        if self.is_black_dot:
            return (
                self.cell1.value is None
                or self.cell2.value is None
                or self.cell1.value == self.cell2.value * 2
                or self.cell2.value == self.cell1.value * 2
            )

        return (
            self.cell1.value is None
            or self.cell2.value is None
            or self.cell1.value == self.cell2.value + 1
            or self.cell1.value == self.cell2.value - 1
        )

    def eliminate(self, board: Board) -> bool:  # noqa: ARG002
        """Automatically complete the Kropki constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        self.logger.debug(
            f"Eliminating candidates for {self.__class__.__name__} constraint",
        )
        eliminated = False

        if self.is_black_dot:
            if self.cell1.value is None and self.cell2.value is None:
                for v1 in set(self.cell1.candidates):
                    possible = False
                    for v2 in self.cell2.candidates:
                        if v1 == v2 * 2 or v2 == v1 * 2:
                            possible = True
                    if not possible:
                        eliminated |= self.cell1.eliminate(v1)

                for v2 in set(self.cell2.candidates):
                    possible = False
                    for v1 in self.cell1.candidates:
                        if v1 == v2 * 2 or v2 == v1 * 2:
                            possible = True
                    if not possible:
                        eliminated |= self.cell2.eliminate(v2)

            elif self.cell1.value is not None and self.cell2.value is None:
                v1 = self.cell1.value
                for v2 in set(self.cell2.candidates):
                    if v1 != v2 * 2 and v2 != v1 * 2:
                        eliminated |= self.cell2.eliminate(v2)

            elif self.cell1.value is None and self.cell2.value is not None:
                v2 = self.cell2.value
                for v1 in set(self.cell1.candidates):
                    if v1 != v2 * 2 and v2 != v1 * 2:
                        eliminated |= self.cell1.eliminate(v1)

        elif not self.is_black_dot:
            if self.cell1.value is None and self.cell2.value is None:
                for v1 in set(self.cell1.candidates):
                    possible = False
                    for v2 in self.cell2.candidates:
                        if v1 == v2 + 1 or v2 == v1 + 1:
                            possible = True
                    if not possible:
                        eliminated |= self.cell1.eliminate(v1)
                for v2 in set(self.cell2.candidates):
                    possible = False
                    for v1 in self.cell1.candidates:
                        if v1 == v2 + 1 or v2 == v1 + 1:
                            possible = True
                    if not possible:
                        eliminated |= self.cell2.eliminate(v2)

            elif self.cell1.value is not None and self.cell2.value is None:
                v1 = self.cell1.value
                for v2 in set(self.cell2.candidates):
                    if v1 != v2 + 1 and v2 != v1 + 1:
                        eliminated |= self.cell2.eliminate(v2)

            elif self.cell1.value is None and self.cell2.value is not None:
                v2 = self.cell2.value
                for v1 in set(self.cell1.candidates):
                    if v1 != v2 + 1 and v2 != v1 + 1:
                        eliminated |= self.cell1.eliminate(v1)
        return eliminated

    def draw(self, gui: SudokuGUI) -> None:
        """Draw this kropki constraint on `gui` if supported.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        color = (0, 0, 0, 255) if self.is_black_dot else (255, 255, 255, 255)

        gui.draw_circle_between_cells(self.cell1, self.cell2, color)

    def deep_copy(self) -> KropkiConstraint:
        """Create a deep copy of the constraint.

        Returns:
            BaseConstraint: A deep copy of the constraint.
        """
        return KropkiConstraint(
            {self.cell1, self.cell2},
            "black" if self.is_black_dot else "white",
        )


# TODO: implement logique quand plusieurs kropki à la suite

# TODO: code plus intelligent mixte par couleur. pas de test de value is None or not en
# amont juste pour chaque boucle soit on fixe la valeur soit on fait une boucle pour
# chaque candidat
