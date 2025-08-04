"""Solving strategies for Sudoku puzzles."""

from src.sudoku.solver.strategies.chain_violation_guard import (
    ChainViolationGuardStrategy,
)
from src.sudoku.solver.strategies.constraint import ConstraintStrategy
from src.sudoku.solver.strategies.elimination import EliminationStrategy
from src.sudoku.solver.strategies.single_hidden import HiddenSingleStrategy
from src.sudoku.solver.strategies.subset_hidden import (
    HiddenPairStrategy,
    HiddenQuadStrategy,
    HiddenTripleStrategy,
)
from src.sudoku.solver.strategies.subset_naked import (
    NakedPairStrategy,
    NakedQuadStrategy,
    NakedTripleStrategy,
)
from src.sudoku.solver.strategies.w_wing import WWingStrategy
from src.sudoku.solver.strategies.x_wing import XWingStrategy

__all__ = [
    "ChainViolationGuardStrategy",
    "ConstraintStrategy",
    "EliminationStrategy",
    "HiddenPairStrategy",
    "HiddenQuadStrategy",
    "HiddenSingleStrategy",
    "HiddenTripleStrategy",
    "NakedPairStrategy",
    "NakedQuadStrategy",
    "NakedTripleStrategy",
    "WWingStrategy",
    "XWingStrategy",
]


# TODO: Locked Set
# TODO: Magic Triple
# TODO: Pair Reduction
# TODO: Violation Prevention
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
# TODO: WXYZ Wing
# TODO: X-Cycles
# TODO: XY-Chain
# TODO: XY-Wing
# TODO: XYZ-Wing

# TODO: strat de variances
