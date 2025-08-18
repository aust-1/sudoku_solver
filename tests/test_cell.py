import pytest

from models import Cell


class TestCell:
    @pytest.fixture
    def cell_pair(self) -> tuple[Cell, Cell]:
        """Provide two linked cells sharing reachability.

        Returns:
            tuple[Cell, Cell]: A pair of linked cells.

        """
        c1 = Cell(0, 0, 9)
        c2 = Cell(0, 1, 9)
        c1.add_reachables([c2])
        c2.add_reachables([c1])
        return c1, c2

    @pytest.fixture
    def filled_cells(self, cell_pair: tuple[Cell, Cell]) -> tuple[Cell, Cell]:
        c1, c2 = cell_pair
        c1.set_value(5)
        return c1, c2

    @pytest.mark.parametrize("row,col", [(0, 0), (2, 5)])
    def test_initialization_and_repr(self, row: int, col: int) -> None:
        cell = Cell(row, col, 9)
        assert cell.row == row and cell.col == col
        assert cell.candidates == set(range(1, 10))
        assert not cell.is_filled()
        assert str(cell) == "."
        assert repr(cell) == f"C{row}.{col}"

    def test_equality_and_reachables(self, cell_pair: tuple[Cell, Cell]) -> None:
        cell, cell_other = cell_pair
        cell_same = Cell(0, 0, 9)
        assert cell_other in cell.reachable_cells
        assert cell not in cell.reachable_cells
        assert cell == cell_same
        assert cell != cell_other
        assert hash(cell) == hash(cell_same)
        assert cell != object()

    @pytest.mark.parametrize("value", [1, 2, 3, 4, 6, 7, 8])
    def test_candidate_elimination(
        self, filled_cells: tuple[Cell, Cell], value: int
    ) -> None:
        c1, c2 = filled_cells
        assert c1.is_filled()
        assert c1.candidates == {5}
        assert 5 not in c2.candidates
        assert not c2.eliminate(5)
        assert c2.eliminate(value)

    def test_final_value_after_eliminations(self, cell_pair: tuple[Cell, Cell]) -> None:
        c1, c2 = cell_pair
        c1.set_value(5)
        for v in [1, 2, 3, 4, 6, 7, 8]:
            c2.eliminate(v)
        assert c2.value == 9
        assert c2.candidates == {9}
