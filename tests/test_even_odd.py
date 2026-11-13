
"""Tests for parity constraints."""

import pytest

from models import Board
from solver.constraints.even_odd import ParityConstraint


def test_string_one_is_converted_to_integer() -> None:
    """Test conversion of string one."""
    board = Board(9)
    constraint = ParityConstraint.from_dict(
        board, {"cell": "a1", "rest": "1"},
    )
    assert constraint.rest == 1


def test_string_zero_is_converted_to_integer() -> None:
    """Test conversion of string zero."""
    board = Board(9)
    constraint = ParityConstraint.from_dict(
        board, {"cell": "a1", "rest": "0"},
    )
    assert constraint.rest == 0


def test_odd_constraint_keeps_only_odd_candidates() -> None:
    """Test that only odd candidates remain."""
    board = Board(9)
    cell = board.get_cell(pos="a1")
    constraint = ParityConstraint.from_dict(
        board, {"cell": "a1", "rest": "1"},
    )

    constraint.eliminate(board)

    assert cell.candidates == {1, 3, 5, 7, 9}


def test_even_constraint_keeps_only_even_candidates() -> None:
    """Test that only even candidates remain."""
    board = Board(9)
    cell = board.get_cell(pos="a1")
    constraint = ParityConstraint.from_dict(
        board, {"cell": "a1", "rest": "0"},
    )

    constraint.eliminate(board)

    assert cell.candidates == {2, 4, 6, 8}


@pytest.mark.parametrize(
    ("rest", "expected"),
    [
        (2, "0 or 1"),
        ("2", "0 or 1"),
        (True, "0 or 1"),
        (None, "0 or 1"),
    ],
)
def test_invalid_parity_value_is_rejected(
    rest: object, expected: str,
) -> None:
    """Test rejection of invalid parity values."""
    board = Board(9)

    with pytest.raises(ValueError, match=expected):
        ParityConstraint.from_dict(
            board, {"cell": "a1", "rest": rest},
        )
