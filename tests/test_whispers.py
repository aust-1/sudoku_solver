from __future__ import annotations

import pytest

from models import Board
from solver.constraints import DutchConstraint, GermanConstraint


@pytest.fixture
def board() -> Board:
    return Board(9)


@pytest.mark.parametrize(("v1", "v2"), [(1, 5), (2, 6), (3, 7), (4, 8), (5, 9)])
def test_dutch_accepts_difference_of_four(board: Board, v1: int, v2: int) -> None:
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = DutchConstraint([e1, e2])
    board.add_constraints(constraint)
    e1.value = v1
    e2.value = v2
    assert constraint.check(board) == set()


def test_dutch_rejects_difference_of_three(board: Board) -> None:
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = DutchConstraint([e1, e2])
    board.add_constraints(constraint)
    e1.value = 1
    e2.value = 4
    assert constraint.check(board) == {e1, e2}


def test_dutch_eliminate_keeps_valid_candidates(board: Board) -> None:
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = DutchConstraint([e1, e2])
    board.add_constraints(constraint)
    e2.candidates = {5}
    constraint.eliminate(board)
    assert e1.candidates == {1, 9}


def test_german_two_cells_keeps_difference_equal_to_five(board: Board) -> None:
    e1 = board.get_cell(pos="e1")
    e2 = board.get_cell(pos="e2")
    constraint = GermanConstraint([e1, e2])
    board.add_constraints(constraint)
    constraint.eliminate(board)
    assert sorted(e1.candidates) == [1, 2, 3, 4, 6, 7, 8, 9]
    assert sorted(e2.candidates) == [1, 2, 3, 4, 6, 7, 8, 9]


def test_german_three_cells_keeps_supported_candidates(board: Board) -> None:
    a1, a2, a3 = (board.get_cell(pos=pos) for pos in ("a1", "a2", "a3"))
    constraint = GermanConstraint([a1, a2, a3])
    board.add_constraints(constraint)
    a1.candidates = {1, 2}
    a3.candidates = {1, 2}
    a2.candidates = {7, 8, 9}
    constraint.eliminate(board)
    assert sorted(a2.candidates) == [7, 8, 9]
    assert a2.value is None


def test_german_three_cells_removes_unsupported_candidates(board: Board) -> None:
    a1, a2, a3 = (board.get_cell(pos=pos) for pos in ("a1", "a2", "a3"))
    constraint = GermanConstraint([a1, a2, a3])
    board.add_constraints(constraint)
    # a1 and a3 see each other, so they cannot both be 1: a2 = 6 would need
    # two distinct neighbours equal to 1.
    a1.candidates = {1, 2}
    a3.candidates = {1, 2}
    a2.candidates = {6, 7}
    constraint.eliminate(board)
    assert a2.value == 7  # noqa: PLR2004
