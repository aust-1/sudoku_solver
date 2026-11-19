from __future__ import annotations

import pytest

from api import app
from models import Board
from solver.constraints import GreaterThanConstraint


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_eliminate_with_empty_candidates_does_not_raise() -> None:
    board = Board(9)
    a1 = board.get_cell(pos="a1")
    a2 = board.get_cell(pos="a2")
    constraint = GreaterThanConstraint(a1, a2)
    board.add_constraints(constraint)
    a1.candidates = set()
    assert constraint.eliminate(board) is False
    assert not board.is_valid()


def test_eliminate_still_reduces_candidates() -> None:
    board = Board(9)
    a1 = board.get_cell(pos="a1")
    a2 = board.get_cell(pos="a2")
    constraint = GreaterThanConstraint(a1, a2)
    board.add_constraints(constraint)
    assert constraint.eliminate(board)
    assert 1 not in a1.candidates
    assert 9 not in a2.candidates  # noqa: PLR2004


def test_board_with_empty_cell_is_invalid() -> None:
    board = Board(9)
    assert board.is_valid()
    board.get_cell(pos="e5").candidates = set()
    assert not board.is_valid()


def test_solve_step_reports_contradiction_as_json(client) -> None:
    response = client.post("/api/board/new", json={"size": 9, "cells": {}})
    board_id = response.get_json()["board_id"]
    response = client.post(
        f"/api/board/{board_id}/constraint",
        json={
            "type": "greater_than",
            "higher_value_cell": "a1",
            "lower_value_cell": "a2",
        },
    )
    assert response.status_code == 200  # noqa: PLR2004
    response = client.put(
        f"/api/board/{board_id}/cell",
        json={"pos": "a2", "value": 9, "candidates": [9]},
    )
    assert response.status_code == 200  # noqa: PLR2004

    for _ in range(2):
        response = client.post(
            f"/api/board/{board_id}/solve/step",
            json={"solver_type": "composite"},
        )
        assert response.status_code == 200  # noqa: PLR2004
        assert response.is_json

    board = response.get_json()["board"]
    assert board["is_valid"] is False
    assert board["is_solved"] is False
