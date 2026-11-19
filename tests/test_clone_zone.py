from __future__ import annotations

from models import Board
from solver.constraints import CloneZoneConstraint, ConstraintType


def _zone_constraint(board: Board) -> CloneZoneConstraint:
    return CloneZoneConstraint(
        [board.get_cell(pos="a1"), board.get_cell(pos="a2")],
        [board.get_cell(pos="e5"), board.get_cell(pos="e6")],
    )


def test_clone_zone_has_its_own_type() -> None:
    constraint = _zone_constraint(Board(9))
    assert constraint.type is ConstraintType.CLONE_ZONE
    assert constraint.to_dict() == {
        "type": "clone_zone",
        "zones": [["a1", "a2"], ["e5", "e6"]],
    }


def test_clone_zone_round_trip_through_board_dict() -> None:
    board = Board(9)
    data = _zone_constraint(board).to_dict()
    reloaded = Board.from_dict({"size": 9, "cells": {}, "constraints": [data]})
    assert [c.to_dict() for c in reloaded.constraints] == [data]
