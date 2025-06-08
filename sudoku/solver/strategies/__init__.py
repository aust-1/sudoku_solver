"""Solving strategies for Sudoku puzzles."""

from sudoku.solver.strategies.constraint import ConstraintStrategy
from sudoku.solver.strategies.elimination import EliminationStrategy
from sudoku.solver.strategies.single_hidden import HiddenSingleStrategy
from sudoku.solver.strategies.single_naked import NakedSingleStrategy
from sudoku.solver.strategies.subset_hidden import (
    HiddenPairStrategy,
    HiddenQuadStrategy,
    HiddenTripleStrategy,
)
from sudoku.solver.strategies.subset_naked import (
    NakedPairStrategy,
    NakedQuadStrategy,
    NakedTripleStrategy,
)

__all__ = [
    "ConstraintStrategy",
    "EliminationStrategy",
    "HiddenPairStrategy",
    "HiddenQuadStrategy",
    "HiddenSingleStrategy",
    "HiddenTripleStrategy",
    "NakedPairStrategy",
    "NakedQuadStrategy",
    "NakedSingleStrategy",
    "NakedTripleStrategy",
]


# TODO: Locked Set
# TODO: Magic Triple
# TODO: Pair Reduction
# TODO: Violation Prevention
# TODO: Chain violation Guard
# TODO: Empty Rectangle
# TODO: Forcing Chain
# TODO: Hidden Unique Rectangle
# TODO: Jollyfish
# TODO: Sashimi-X-Wing
# TODO: Simple Coloring
# TODO: Swordfish
# TODO: 3D Medusa
# TODO: Two-String-Kite
# TODO: Unique Rectangle
# TODO: W-Wing
# TODO: WXYZ Wing
# TODO: X-Cycles
# TODO: X-Wing
# TODO: XY-Chain
# TODO: XY-Wing
# TODO: XYZ-Wing

# TODO: strat de variances
