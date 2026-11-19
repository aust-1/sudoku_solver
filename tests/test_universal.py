from __future__ import annotations

from models import Board
from solver.constraints import UniversalConstraint

SOLVED_UNIVERSAL = (
    # Every row, column, box and same-position-in-box group holds 1-9 once.
    "123456789"
    "456789123"
    "789123456"
    "231564897"
    "564897231"
    "897231564"
    "312645978"
    "645978312"
    "978312645"
)


def test_universal_accepts_different_values_in_a_group() -> None:
    board = Board(9)
    constraint = UniversalConstraint()
    board.add_constraints(constraint)
    board.get_cell(pos="a1").value = 1
    board.get_cell(pos="d4").value = 2
    assert constraint.check(board) == set()
    assert board.is_valid()


def test_universal_rejects_equal_values_in_a_group() -> None:
    board = Board(9)
    constraint = UniversalConstraint()
    board.add_constraints(constraint)
    a1 = board.get_cell(pos="a1")
    d4 = board.get_cell(pos="d4")
    a1.value = 1
    # Bypass the setter propagation to build an invalid grid on purpose.
    d4.candidates = {1}
    d4._value = 1  # noqa: SLF001
    assert constraint.check(board) == {a1, d4}
    assert not board.is_valid()


def test_universal_full_grid_is_solved() -> None:
    board = Board(9)
    board.add_constraints(UniversalConstraint())
    board.load_from_string(SOLVED_UNIVERSAL)
    assert board.is_valid()
    assert board.is_solved()
