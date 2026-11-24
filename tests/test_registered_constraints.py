from __future__ import annotations

import pytest

from api import app
from models import Board
from solver.constraints import (
    AxiaConstraint,
    CoupleConstraint,
    FriendlyCellConstraint,
)
from solver.constraints.factory import CONSTRAINT_REGISTRY


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def _load(constraint: dict) -> Board:
    return Board.from_dict({"size": 9, "cells": {}, "constraints": [constraint]})


@pytest.mark.parametrize(
    ("data", "cls"),
    [
        ({"type": "axia", "cell": "e5"}, AxiaConstraint),
        ({"type": "couple", "cell1": "a1", "cell2": "a2", "same": True}, CoupleConstraint),
        ({"type": "couple", "cell1": "a1", "cell2": "b1", "same": False}, CoupleConstraint),
        ({"type": "friendly_cell", "cell": "c4"}, FriendlyCellConstraint),
    ],
)
def test_constraint_loads_from_json(data: dict, cls: type) -> None:
    board = _load(data)
    (constraint,) = board.constraints
    assert isinstance(constraint, cls)
    assert constraint.to_dict() == data


@pytest.mark.parametrize("name", ["axia", "couple", "friendly_cell"])
def test_constraint_is_registered(name: str) -> None:
    assert name in CONSTRAINT_REGISTRY


def test_friendly_cell_accepts_row_column_or_box_number() -> None:
    # c4: row 3, column 4, box 2.
    for value in (2, 3, 4):
        board = Board(9)
        cell = board.get_cell(pos="c4")
        constraint = FriendlyCellConstraint(cell)
        board.add_constraints(constraint)
        cell.value = value
        assert constraint.check(board) == set()
        assert board.is_valid()


def test_friendly_cell_rejects_other_values() -> None:
    board = Board(9)
    cell = board.get_cell(pos="c4")
    constraint = FriendlyCellConstraint(cell)
    board.add_constraints(constraint)
    cell.value = 7
    assert constraint.check(board) == {cell}


def test_friendly_cell_issue_example() -> None:
    board = Board(9)
    a1 = board.get_cell(pos="a1")
    constraint = FriendlyCellConstraint(a1)
    a1.value = 1
    assert constraint.check(board) == set()


@pytest.mark.parametrize("same", ["true", 1, None])
def test_couple_rejects_non_boolean_same(same: object) -> None:
    with pytest.raises(ValueError, match="'same' must be true or false"):
        _load({"type": "couple", "cell1": "a1", "cell2": "a2", "same": same})


@pytest.mark.parametrize(
    "zones",
    [
        [["a1", "a2"]],
        [["a1", "a2"], []],
        [["a1", "a2"], ["e5"]],
        "a1",
    ],
)
def test_clone_zone_rejects_invalid_zones(zones: object) -> None:
    with pytest.raises(ValueError, match="CloneZone constraint"):
        _load({"type": "clone_zone", "zones": zones})


def test_clone_zone_from_api(client) -> None:
    board_id = client.post("/api/board/new", json={"size": 9, "cells": {}}).get_json()[
        "board_id"
    ]
    response = client.post(
        f"/api/board/{board_id}/constraint",
        json={"type": "clone_zone", "zones": [["a1", "a2"], ["e5", "e6"]]},
    )
    assert response.status_code == 200  # noqa: PLR2004
    response = client.post(
        f"/api/board/{board_id}/constraint",
        json={"type": "clone_zone", "cells": ["a1", "a2"]},
    )
    assert response.status_code == 400  # noqa: PLR2004


def test_catalog_lists_new_constraints_with_selection_help(client) -> None:
    constraints = client.get("/api/constraints").get_json()["constraints"]
    by_id = {c["id"]: c for c in constraints}
    for name in ("axia", "couple", "friendly_cell", "clone_zone"):
        assert name in by_id
    assert "Validate zone" in by_id["clone_zone"]["description"]
    for constraint in constraints:
        assert "Select" in constraint["description"] or "No selection" in constraint[
            "description"
        ]
