import pytest

from models import Board, Cell
from solver.constraints.frienly_cell import FriendlyCellConstraint


class TestFriendlyCellCheck:
    @pytest.mark.parametrize("value", [2, 4, 5])
    def test_value_matching_row_col_or_box_is_valid(self, value: int) -> None:
        # b5 is row index 4, column index 1, box index 3: its friendly digits are 5, 2 and 4.
        cell = Cell(4, 1, 9)
        cell.value = value
        constraint = FriendlyCellConstraint(cell)

        assert constraint.check(Board(9)) == set()

    @pytest.mark.parametrize("value", [1, 3, 6, 7, 8, 9])
    def test_value_matching_none_of_row_col_or_box_is_invalid(self, value: int) -> None:
        cell = Cell(4, 1, 9)
        cell.value = value
        constraint = FriendlyCellConstraint(cell)

        assert constraint.check(Board(9)) == {cell}

    def test_empty_cell_is_not_reported(self) -> None:
        cell = Cell(4, 1, 9)
        constraint = FriendlyCellConstraint(cell)

        assert constraint.check(Board(9)) == set()
