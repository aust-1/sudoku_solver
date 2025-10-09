"""Quick test script to verify the API is working."""

import json

import requests

API_BASE = "http://localhost:5000/api"


def test_api():
    """Test basic API functionality."""
    print("Testing API endpoints...\n")

    # Test 1: List constraints
    print("1. Testing GET /api/constraints")
    response = requests.get(f"{API_BASE}/constraints", timeout=5)
    print(f"   Status: {response.status_code}")
    constraints = response.json()["constraints"]
    print(f"   Found {len(constraints)} constraint types")
    print(f"   Examples: {[c['id'] for c in constraints[:3]]}")

    # Test 2: Create a new board
    print("\n2. Testing POST /api/board/new")
    board_data = {
        "size": 9,
        "cells": {"a1": [1, 2, 3], "a2": [5], "b1": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
        "constraint": [{"type": "knight"}],
    }
    response = requests.post(
        f"{API_BASE}/board/new", json=board_data, timeout=5
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    board_id = data["board_id"]
    print(f"   Board ID: {board_id}")
    print(f"   Is valid: {data['board']['is_valid']}")
    print(f"   Is solved: {data['board']['is_solved']}")

    # Test 3: Get board state
    print(f"\n3. Testing GET /api/board/{board_id}")
    response = requests.get(f"{API_BASE}/board/{board_id}", timeout=5)
    print(f"   Status: {response.status_code}")
    board = response.json()["board"]
    print(f"   Board size: {board['size']}")
    print(f"   Number of cells: {len(board['cells'])}")

    # Test 4: Solve a step
    print(f"\n4. Testing POST /api/board/{board_id}/solve/step")
    response = requests.post(
        f"{API_BASE}/board/{board_id}/solve/step",
        json={"solver_type": "composite"},
        timeout=5,
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Changed: {result['changed']}")
    print(f"   Solved: {result['solved']}")
    print(f"   Solver used: {result['log']['solver']}")
    if result["log"]["changes"]:
        print(f"   Number of changes: {len(result['log']['changes'])}")

    # Test 5: Update a cell
    print(f"\n5. Testing PUT /api/board/{board_id}/cell")
    response = requests.put(
        f"{API_BASE}/board/{board_id}/cell",
        json={"pos": "a1", "value": 5},
        timeout=5,
    )
    print(f"   Status: {response.status_code}")
    board = response.json()["board"]
    cell_a1 = next(c for c in board["cells"] if c["pos"] == "a1")
    print(f"   Cell a1 value: {cell_a1['value']}")
    print(f"   Cell a1 is filled: {cell_a1['is_filled']}")

    # Test 6: Get logs
    print(f"\n6. Testing GET /api/board/{board_id}/logs")
    response = requests.get(f"{API_BASE}/board/{board_id}/logs", timeout=5)
    print(f"   Status: {response.status_code}")
    logs = response.json()["logs"]
    print(f"   Number of log entries: {len(logs)}")

    print("\n✅ All API tests passed!")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API. Make sure the server is running:")
        print("   uv run python src/api.py")
    except Exception as e:
        print(f"❌ Error: {e}")
