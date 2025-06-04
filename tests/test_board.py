import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.board import Board

def test_import_board():
    # Simple sanity check that Board can be imported and instantiated
    b = Board()
    assert b.is_full() is False


def test_self_exclude_constraint():
    b = Board()
    # force duplicate values in excluded set
    b._grid._grid[0][0].set_value(1)
    b._grid._grid[0][1].set_value(1)
    assert b.check_constraints() is False


def test_get_reachable_pieces():
    b = Board()
    reachable = b.get_reachable_pieces((0, 1))
    assert (0, 0) in reachable
    assert (1, 0) in reachable
    # number of unique positions from row 0 and column 0 minus duplicates
    assert len(reachable) == 16
