from __future__ import annotations

import pytest

import api
from api import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def _new_board(client, payload: dict | None = None) -> str:
    response = client.post("/api/board/new", json=payload or {"size": 9, "cells": {}})
    assert response.status_code == 200  # noqa: PLR2004
    return response.get_json()["board_id"]


def test_delete_board(client) -> None:
    board_id = _new_board(client)
    response = client.delete(f"/api/board/{board_id}")
    assert response.status_code == 200  # noqa: PLR2004
    assert board_id not in api.boards
    assert board_id not in api.board_logs
    assert board_id not in api.board_constraints
    assert client.get(f"/api/board/{board_id}").status_code == 404  # noqa: PLR2004
    assert client.delete(f"/api/board/{board_id}").status_code == 404  # noqa: PLR2004


def test_board_count_is_bounded(client, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(api, "MAX_BOARDS", 3)
    ids = [_new_board(client) for _ in range(5)]
    assert len(api.boards) <= 3  # noqa: PLR2004
    # The most recent boards are kept, the oldest ones are evicted.
    assert ids[-1] in api.boards
    assert ids[0] not in api.boards


def test_least_recently_used_board_is_evicted(
    client, monkeypatch: pytest.MonkeyPatch
) -> None:
    for board_id in list(api.boards):
        api._forget_board(board_id)  # noqa: SLF001
    monkeypatch.setattr(api, "MAX_BOARDS", 2)
    first = _new_board(client)
    second = _new_board(client)
    client.get(f"/api/board/{first}")  # first becomes the most recently used
    third = _new_board(client)
    assert first in api.boards
    assert third in api.boards
    assert second not in api.boards


def test_expired_board_is_dropped(client, monkeypatch: pytest.MonkeyPatch) -> None:
    board_id = _new_board(client)
    api.board_last_access[board_id] -= api.BOARD_TTL_SECONDS + 1
    assert client.get(f"/api/board/{board_id}").status_code == 404  # noqa: PLR2004
    assert board_id not in api.boards


def test_logs_are_bounded(client, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(api, "MAX_LOGS_PER_BOARD", 3)
    board_id = _new_board(client)
    for _ in range(5):
        client.post(
            f"/api/board/{board_id}/solve/step", json={"solver_type": "simple"}
        )
    logs = client.get(f"/api/board/{board_id}/logs").get_json()["logs"]
    assert len(logs) == 3  # noqa: PLR2004


def test_export_is_per_board(client) -> None:
    first = _new_board(client, {"size": 9, "cells": {"a1": [1, 2]}})
    second = _new_board(client, {"size": 9, "cells": {"a1": [3, 4]}})
    assert client.get(f"/api/board/{first}/export").get_json()["cells"]["a1"] == [
        1,
        2,
    ]
    assert client.get(f"/api/board/{second}/export").get_json()["cells"]["a1"] == [
        3,
        4,
    ]


def test_export_follows_constraint_deletion(client) -> None:
    board_id = _new_board(client)
    client.post(f"/api/board/{board_id}/constraint", json={"type": "king"})
    client.delete(f"/api/board/{board_id}/constraint/0")
    exported = client.get(f"/api/board/{board_id}/export").get_json()
    assert exported["constraints"] == []


def test_import_returns_a_usable_board_id(client) -> None:
    response = client.post(
        "/api/board/import",
        json={"size": 9, "cells": {"a1": [1, 2]}, "constraints": [{"type": "king"}]},
    )
    board_id = response.get_json()["board_id"]
    response = client.post(
        f"/api/board/{board_id}/solve/step", json={"solver_type": "simple"}
    )
    assert response.status_code == 200  # noqa: PLR2004


def test_global_board_routes_are_gone(client) -> None:
    assert client.get("/api/board").status_code in {404, 405}


def test_reset_replaces_board_and_clears_logs(client) -> None:
    board_id = _new_board(client)
    initial = client.get(f"/api/board/{board_id}/export").get_json()
    client.put(f"/api/board/{board_id}/cell", json={"pos": "e5", "value": 7})
    client.post(f"/api/board/{board_id}/solve/step", json={"solver_type": "simple"})
    assert client.get(f"/api/board/{board_id}/logs").get_json()["logs"]

    response = client.post(f"/api/board/{board_id}/reset", json=initial)
    assert response.status_code == 200  # noqa: PLR2004
    board = response.get_json()["board"]
    e5 = next(cell for cell in board["cells"] if cell["pos"] == "e5")
    assert e5["value"] is None
    assert e5["candidates"] == list(range(1, 10))
    assert client.get(f"/api/board/{board_id}/logs").get_json()["logs"] == []


def test_reset_rejects_invalid_state(client) -> None:
    board_id = _new_board(client)
    response = client.post(f"/api/board/{board_id}/reset", json={"size": "x"})
    assert response.status_code == 400  # noqa: PLR2004
    assert client.get(f"/api/board/{board_id}").status_code == 200  # noqa: PLR2004
