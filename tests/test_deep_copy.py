from __future__ import annotations

from models import Board
from solver.constraints import (
    CloneConstraint,
    GermanConstraint,
    KillerConstraint,
    KropkiConstraint,
    PalindromeConstraint,
)
from solver.strategies import ConstraintStrategy


def test_deep_copy_does_not_modify_original_board() -> None:
    board = Board(9)
    board.add_constraints(
        KropkiConstraint.black(board.get_cell(pos="a1"), board.get_cell(pos="a2")),
    )
    copy = board.deep_copy()
    copy.get_cell(pos="a1").value = 3
    ConstraintStrategy().apply(copy)

    assert board.get_cell(pos="a1").candidates == set(range(1, 10))
    assert board.get_cell(pos="a2").candidates == set(range(1, 10))
    assert copy.get_cell(pos="a2").value == 6  # noqa: PLR2004


def test_deep_copy_constraints_use_copied_cells() -> None:
    board = Board(9)
    a1, a2, a3 = (board.get_cell(pos=pos) for pos in ("a1", "a2", "a3"))
    board.add_constraints(
        KropkiConstraint.white(a1, a2),
        GermanConstraint([a1, a2, a3]),
        PalindromeConstraint([board.get_cell(pos="b1"), board.get_cell(pos="b3")]),
        KillerConstraint({board.get_cell(pos="c1"), board.get_cell(pos="c2")}, 3, 9),
        CloneConstraint({board.get_cell(pos="d1"), board.get_cell(pos="f5")}),
    )
    copy = board.deep_copy()
    copy_cells = {id(cell) for cell in copy.get_all_cells()}
    original_cells = {id(cell) for cell in board.get_all_cells()}

    for constraint in copy.constraints:
        for value in vars(constraint).values():
            items = value if isinstance(value, (list, set)) else [value]
            for item in items:
                if hasattr(item, "candidates"):
                    assert id(item) in copy_cells
                    assert id(item) not in original_cells


def test_deep_copy_applies_local_constraints_to_copy() -> None:
    board = Board(9)
    # a1 and e5 share no row, column or box: they are the two ends of a palindrome.
    board.add_constraints(
        PalindromeConstraint([board.get_cell(pos="a1"), board.get_cell(pos="e5")]),
    )
    copy = board.deep_copy()
    copy.get_cell(pos="a1").value = 4
    ConstraintStrategy().apply(copy)

    assert copy.get_cell(pos="e5").value == 4  # noqa: PLR2004
    assert board.get_cell(pos="a1").value is None
    assert board.get_cell(pos="e5").value is None
