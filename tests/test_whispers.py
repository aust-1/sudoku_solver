"""Tests for the German and Dutch whisper constraints."""

from __future__ import annotations

import pytest

from models import Board
from solver.constraints import DutchConstraint, GermanConstraint


@pytest.mark.parametrize(
    ("first", "second"),
    [(1, 5), (2, 6), (3, 7), (4, 8), (5, 9), (1, 9), (9, 4)],
)
def test_dutch_check_accepts_difference_of_at_least_four(
    first: int,
    second: int,
) -> None:
    """Neighbouring Dutch whisper cells may differ by exactly 4 or more."""
    board = Board(9)
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = DutchConstraint([e1, e2])

    e1.value = first
    e2.value = second

    assert constraint.check(board) == set()


@pytest.mark.parametrize(("first", "second"), [(1, 4), (5, 2), (6, 9), (5, 5)])
def test_dutch_check_rejects_difference_below_four(first: int, second: int) -> None:
    """Neighbouring Dutch whisper cells closer than 4 are flagged."""
    board = Board(9)
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = DutchConstraint([e1, e2])

    e1.value = first
    e2.value = second

    assert constraint.check(board) == {e1, e2}


def test_german_check_still_requires_difference_of_five() -> None:
    """German whispers keep their minimum difference of 5."""
    board = Board(9)
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = GermanConstraint([e1, e2])

    e1.value = 1
    e2.value = 5
    assert constraint.check(board) == {e1, e2}

    e2.value = 6
    assert constraint.check(board) == set()


def test_dutch_deep_copy_keeps_difference() -> None:
    """A deep-copied Dutch constraint keeps the difference of 4."""
    board = Board(9)
    constraint = DutchConstraint([board.get_cell(pos="e1"), board.get_cell(pos="e2")])

    assert constraint.deep_copy().diff == 4
