"""Solving strategies for Sudoku puzzles."""

from .constraint import ConstraintStrategy
from .elimination import EliminationStrategy
from .single_choice import SingleChoiceStrategy
from .single_candidate import SingleCandidateStrategy
from .subset_choice import (
    PairChoiceStrategy,
    QuadChoiceStrategy,
    TripleChoiceStrategy,
)
from .subset_candidate import (
    PairCandidateStrategy,
    QuadCandidateStrategy,
    TripleCandidateStrategy,
)

__all__ = [
    "ConstraintStrategy",
    "EliminationStrategy",
    "SingleChoiceStrategy",
    "SingleCandidateStrategy",
    "PairChoiceStrategy",
    "TripleChoiceStrategy",
    "QuadChoiceStrategy",
    "PairCandidateStrategy",
    "TripleCandidateStrategy",
    "QuadCandidateStrategy",
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
