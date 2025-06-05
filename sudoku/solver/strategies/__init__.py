"""Solving strategies for Sudoku puzzles."""

from .single_candidate import SingleCandidateStrategy
from .only_choice import OnlyChoiceStrategy
from .elimination import EliminationStrategy

__all__ = [
    "SingleCandidateStrategy",
    "OnlyChoiceStrategy",
    "EliminationStrategy",
]
