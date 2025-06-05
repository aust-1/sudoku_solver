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
# TODO: rajouter les autres stratégies
