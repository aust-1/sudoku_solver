from __future__ import annotations

import pytest

from api import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def _cell(board_json: dict, pos: str) -> dict:
    return next(cell for cell in board_json["cells"] if cell["pos"] == pos)


def _new_board(client, cells: dict | None = None) -> tuple[str, dict]:
    response = client.post("/api/board/new", json={"size": 9, "cells": cells or {}})
    data = response.get_json()
    return data["board_id"], data["board"]


def test_new_board_has_no_given(client) -> None:
    _, board = _new_board(client)
    assert all(cell["is_given"] is False for cell in board["cells"])


def test_setup_digit_is_given(client) -> None:
    board_id, _ = _new_board(client)
    response = client.put(
        f"/api/board/{board_id}/cell",
        json={"pos": "a1", "value": 4, "candidates": [4], "given": True},
    )
    board = response.get_json()["board"]
    a1 = _cell(board, "a1")
    assert a1["value"] == 4  # noqa: PLR2004
    assert a1["is_given"] is True
    assert 4 not in _cell(board, "a2")["candidates"]  # noqa: PLR2004


def test_solver_digit_is_not_given(client) -> None:
    board_id, _ = _new_board(client)
    response = client.put(
        f"/api/board/{board_id}/cell", json={"pos": "a1", "value": 4}
    )
    assert _cell(response.get_json()["board"], "a1")["is_given"] is False


def test_clearing_a_given_digit(client) -> None:
    board_id, _ = _new_board(client)
    client.put(
        f"/api/board/{board_id}/cell",
        json={"pos": "a1", "value": 4, "candidates": [4], "given": True},
    )
    response = client.put(
        f"/api/board/{board_id}/cell",
        json={"pos": "a1", "value": None, "candidates": list(range(1, 10)), "given": False},
    )
    a1 = _cell(response.get_json()["board"], "a1")
    assert a1["value"] is None
    assert a1["is_given"] is False


def test_imported_single_candidates_are_given_digits(client) -> None:
    _, board = _new_board(client, {"a1": [4], "e5": [7], "b2": [1, 2]})
    for pos, value in (("a1", 4), ("e5", 7)):
        cell = _cell(board, pos)
        assert cell["value"] == value
        assert cell["is_filled"] is True
        assert cell["is_given"] is True
    assert _cell(board, "b2")["is_given"] is False
    assert 4 not in _cell(board, "a2")["candidates"]  # noqa: PLR2004


def test_solver_step_does_not_create_given_digits(client) -> None:
    board_id, _ = _new_board(client, {"a1": [4], "a2": [1, 2], "a3": [1, 2]})
    response = client.post(
        f"/api/board/{board_id}/solve/step", json={"solver_type": "simple"}
    )
    board = response.get_json()["board"]
    given = {cell["pos"] for cell in board["cells"] if cell["is_given"]}
    assert given == {"a1"}
