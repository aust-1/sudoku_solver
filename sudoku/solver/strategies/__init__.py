"""Solving strategies for Sudoku puzzles."""

from sudoku.solver.strategies.constraint import ConstraintStrategy
from sudoku.solver.strategies.elimination import EliminationStrategy
from sudoku.solver.strategies.single_candidate import SingleCandidateStrategy
from sudoku.solver.strategies.single_choice import SingleChoiceStrategy
from sudoku.solver.strategies.subset_candidate import (
    PairCandidateStrategy,
    QuadCandidateStrategy,
    TripleCandidateStrategy,
)
from sudoku.solver.strategies.subset_choice import (
    PairChoiceStrategy,
    QuadChoiceStrategy,
    TripleChoiceStrategy,
)

__all__ = [
    "ConstraintStrategy",
    "EliminationStrategy",
    "PairCandidateStrategy",
    "PairChoiceStrategy",
    "QuadCandidateStrategy",
    "QuadChoiceStrategy",
    "SingleCandidateStrategy",
    "SingleChoiceStrategy",
    "TripleCandidateStrategy",
    "TripleChoiceStrategy",
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
