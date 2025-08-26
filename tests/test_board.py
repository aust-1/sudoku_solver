from __future__ import annotations

from typing import override

import pytest

from models import Board, Cell
from solver.constraints import BaseConstraint


class DummyConstraint(BaseConstraint):
    """A dummy constraint for testing purposes.

    Args:
        BaseConstraint (ABC): The abstract base class for all constraints.

    """

    def __init__(self, check_result: bool = True) -> None:
        """Initialize the dummy constraint.

        Args:
            check_result (bool, optional): The result to return for the check method.
                Defaults to True.

        """
        super().__init__()
        self.check_result = check_result

    @override
    def check(self, board: Board) -> bool:
        """Check if the constraint is satisfied on the given board.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool:
                ``True`` if the constraint is satisfied, ``False`` otherwise.

        """
        return self.check_result

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated, ``False`` otherwise.

        """
        return False

    @override
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.

        """
        return {board.get_cell(cell.row, (cell.col + 1) % board.size)}

    @override
    def get_regions(self, board: Board) -> dict[str, set[Cell]]:
        """Get the regions defined by the constraint.

        Args:
            board (Board): The Sudoku board.

        Returns:
            dict[str,set[Cell]]: A dictionary mapping region names to sets of cells.

        """
        return {"dummy": {board.get_cell(row=0, col=0)}}

    @override
    def deep_copy(self) -> DummyConstraint:
        """Create a deep copy of the constraint.

        Returns:
            DummyConstraint: A deep copy of the constraint.

        """
        return DummyConstraint(self.check_result)


class TestBoard:
    @pytest.fixture
    def empty_board(self) -> Board:
        return Board(9)

    @pytest.fixture
    def sample_puzzle(self) -> str:
        return (
            "530070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )

    @pytest.fixture
    def sample_solved(self) -> str:
        return (
            "534678912"
            "672195348"
            "198342567"
            "859761423"
            "426853791"
            "713924856"
            "961537284"
            "287419635"
            "345286179"
        )

    @pytest.fixture
    def solved_board(self, sample_solved: str) -> Board:
        b = Board(9)
        b.load_from_string(sample_solved)
        return b

    @pytest.fixture
    def invalid_board(self) -> Board:
        b = Board(9)
        b.get_cell(row=0, col=0).value = 1
        b.get_cell(row=0, col=1).value = 1
        return b

    @pytest.mark.parametrize("getter", ["_get_row", "_get_col", "_get_box"])
    def test_region_lengths(self, empty_board: Board, getter: str) -> None:
        region = getattr(empty_board, getter)(0)
        assert len(region) == empty_board.size

    def test_get_cell_and_all_cells(self, empty_board: Board) -> None:
        assert empty_board.get_cell(row=0, col=0) in empty_board._get_row(0)
        assert len(list(empty_board.get_all_cells())) == empty_board.size**2

    def test_add_constraint_and_reachability(self, empty_board: Board) -> None:
        constraint = DummyConstraint()
        empty_board.add_constraints(constraint)
        empty_board._init_regions()
        empty_board._init_reachability()
        cell = empty_board.get_cell(row=0, col=0)
        next_cell = empty_board.get_cell(row=0, col=1)
        assert next_cell in cell.reachable_cells
        assert "dummy" in empty_board.regions

    def test_load_and_str(self, empty_board: Board, sample_puzzle: str) -> None:
        empty_board.load_from_string(sample_puzzle)
        assert empty_board.get_cell(row=0, col=0).value == 5
        board_str = str(empty_board)
        assert board_str.splitlines()[0].startswith("5 3")

    def test_is_valid_and_is_solved(
        self, solved_board: Board, invalid_board: Board
    ) -> None:
        assert solved_board.is_valid()
        assert solved_board.is_solved()
        assert not invalid_board.is_valid()
        assert not invalid_board.is_solved()
        constraint_fail = DummyConstraint(False)
        solved_board.add_constraints(constraint_fail)
        assert not solved_board.is_valid()

    @pytest.mark.parametrize("check_result", [True, False])
    def test_constraint_validation(
        self, sample_solved: str, check_result: bool
    ) -> None:
        board = Board(9)
        board.load_from_string(sample_solved)
        board.add_constraints(DummyConstraint(check_result))
        assert board.is_valid() is check_result

    def test_deep_copy_and_copy_values(self, sample_puzzle: str) -> None:
        board = Board(9)
        board.load_from_string(sample_puzzle)
        board.add_constraints(DummyConstraint())
        clone = board.deep_copy()
        assert clone is not board
        assert clone.get_cell(row=0, col=0).value == board.get_cell(row=0, col=0).value
        assert len(clone.constraints) == len(board.constraints)
        clone.get_cell(row=0, col=0).value = 9
        assert board.get_cell(row=0, col=0).value != clone.get_cell(row=0, col=0).value
        board.get_cell(row=0, col=2).candidates = {1, 2}
        board2 = Board(9)
        board2.copy_values_from(board)
        assert board2.get_cell(row=0, col=0).value == board.get_cell(row=0, col=0).value
        assert board2.get_cell(row=0, col=2).candidates == {1, 2}
