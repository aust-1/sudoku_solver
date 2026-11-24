"""API scenarios formerly run by hand with ``test_api.py`` and a live server."""

from __future__ import annotations

import pytest

from api import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def board_id(client) -> str:
    response = client.post(
        "/api/board/new",
        json={
            "size": 9,
            "cells": {"a1": [1, 2, 3], "a2": [5], "b1": list(range(1, 10))},
            # Legacy key, still accepted by the API.
            "constraint": [{"type": "knight"}],
        },
    )
    assert response.status_code == 200  # noqa: PLR2004
    data = response.get_json()
    assert isinstance(data["board"]["is_valid"], bool)
    assert data["board"]["is_solved"] is False
    return data["board_id"]


def test_list_constraints(client) -> None:
    response = client.get("/api/constraints")
    assert response.status_code == 200  # noqa: PLR2004
    constraints = response.get_json()["constraints"]
    ids = {c["id"] for c in constraints}
    assert {"knight", "king", "killer", "xv"} <= ids
    for constraint in constraints:
        assert set(constraint) == {"id", "name", "description"}


def test_new_board_without_body_is_empty_9x9(client) -> None:
    response = client.post("/api/board/new")
    assert response.status_code == 200  # noqa: PLR2004
    board = response.get_json()["board"]
    assert board["size"] == 9  # noqa: PLR2004
    assert len(board["cells"]) == 81  # noqa: PLR2004
    assert all(not cell["is_filled"] for cell in board["cells"])


def test_get_board_state(client, board_id: str) -> None:
    response = client.get(f"/api/board/{board_id}")
    assert response.status_code == 200  # noqa: PLR2004
    board = response.get_json()["board"]
    assert board["size"] == 9  # noqa: PLR2004
    assert len(board["cells"]) == 81  # noqa: PLR2004
    assert board["constraints"] == [{"type": "knight"}]


PUZZLE = (
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
def puzzle_board_id(client) -> str:
    cells = {
        f"{chr(ord('a') + idx // 9)}{idx % 9 + 1}": [int(digit)]
        for idx, digit in enumerate(PUZZLE)
        if digit != "0"
    }
    response = client.post("/api/board/new", json={"size": 9, "cells": cells})
    return response.get_json()["board_id"]


@pytest.mark.parametrize("solver_type", ["simple", "composite", "backtracking"])
def test_solve_step(client, puzzle_board_id: str, solver_type: str) -> None:
    response = client.post(
        f"/api/board/{puzzle_board_id}/solve/step",
        json={"solver_type": solver_type},
    )
    assert response.status_code == 200  # noqa: PLR2004
    result = response.get_json()
    assert isinstance(result["changed"], bool)
    assert isinstance(result["solved"], bool)
    assert result["log"]["action"] == "solve_step"
    assert result["log"]["changed"] == result["changed"]
    assert isinstance(result["log"]["changes"], list)
    assert result["board"]["is_valid"] is True


def test_update_cell(client, board_id: str) -> None:
    response = client.put(
        f"/api/board/{board_id}/cell",
        json={"pos": "a1", "value": 1},
    )
    assert response.status_code == 200  # noqa: PLR2004
    board = response.get_json()["board"]
    cell_a1 = next(c for c in board["cells"] if c["pos"] == "a1")
    assert cell_a1["value"] == 1
    assert cell_a1["is_filled"] is True


def test_logs_record_each_step(client, board_id: str) -> None:
    assert client.get(f"/api/board/{board_id}/logs").get_json()["logs"] == []
    for _ in range(2):
        client.post(
            f"/api/board/{board_id}/solve/step",
            json={"solver_type": "simple"},
        )
    response = client.get(f"/api/board/{board_id}/logs")
    assert response.status_code == 200  # noqa: PLR2004
    logs = response.get_json()["logs"]
    assert len(logs) == 2  # noqa: PLR2004
    assert all(entry["solver"] == "EliminationStrategy" for entry in logs)


def test_add_and_delete_constraint(client, board_id: str) -> None:
    response = client.post(f"/api/board/{board_id}/constraint", json={"type": "king"})
    assert response.status_code == 200  # noqa: PLR2004
    assert response.get_json()["board"]["constraints"] == [
        {"type": "knight"},
        {"type": "king"},
    ]
    response = client.delete(f"/api/board/{board_id}/constraint/1")
    assert response.status_code == 200  # noqa: PLR2004
    assert response.get_json()["board"]["constraints"] == [{"type": "knight"}]


def test_delete_constraint_out_of_range(client, board_id: str) -> None:
    response = client.delete(f"/api/board/{board_id}/constraint/5")
    assert response.status_code == 400  # noqa: PLR2004
    assert "error" in response.get_json()
