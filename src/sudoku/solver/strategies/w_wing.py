from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class WWingStrategy(Solver):
    """Eliminate candidates using the W-Wing technique."""

    def apply(self, board: Board) -> bool:
        """Apply the W-Wing strategy to the board.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: ``True`` if any candidates were eliminated, ``False`` otherwise.

        """
        self.logger.debug("WWingStrategy running")
        moved = False

        for digit in range(1, board.size + 1):
            strong_links: set[tuple[Cell, Cell]] = set()
            for region in (r for r in board.regions.values() if len(r) == board.size):
                cells = [
                    cell
                    for cell in region
                    if not cell.is_filled() and digit in cell.candidates
                ]
                if len(cells) == 2:  # noqa: PLR2004
                    strong_links.add((cells[0], cells[1]))

            moved |= self._process_strong_links_w_wing(digit, strong_links)

        return moved

    def _process_strong_links_w_wing(
        self,
        digit: int,
        strong_links: set[tuple[Cell, Cell]],
    ) -> bool:
        """Process strong links for the W-Wing strategy.

        Args:
            digit (int): The digit being considered.
            strong_links (set[tuple[Cell, Cell]]): The strong links to process.

        Returns:
            bool: ``True`` if any candidates were eliminated, ``False`` otherwise.

        """
        moved = False
        for a, b in strong_links:
            for j in set(a.reachable_cells):
                if (
                    j.is_filled()
                    or len(j.candidates) != 2  # noqa: PLR2004
                    or digit not in j.candidates
                ):
                    continue
                for k in set(b.reachable_cells):
                    if (
                        k.is_filled()
                        or len(k.candidates) != 2  # noqa: PLR2004
                        or digit not in k.candidates
                        or set(j.candidates) != set(k.candidates)
                    ):
                        continue

                    targets = a.reachable_cells.intersection(b.reachable_cells)
                    value = (j.candidates - {digit}).pop()
                    eliminated = False
                    for cell in targets:
                        eliminated |= cell.eliminate(value)
                    if eliminated:
                        moved = True
                        self.logger.debug(
                            f"Eliminated due to W-Wing with {j}, {k}, {a}, {b}",
                        )

        return moved
