"""Model classes for Sudoku constraints."""

from .base_constraint import BaseConstraint
from .clone_constraint import CloneConstraint
from .clone_zone_constraint import CloneZoneConstraint
from .king_constraint import KingConstraint
from .knight_constraint import KnightConstraint
from .palindrome_constraint import PalindromeConstraint

__all__ = [
    "BaseConstraint",
    "CloneConstraint",
    "CloneZoneConstraint",
    "KingConstraint",
    "KnightConstraint",
    "PalindromeConstraint",
]

# TODO: Arrow
# TODO: Ascending Sequences
# TODO: Between Lines
# TODO: Bishop
# TODO: Consecutive
# TODO: Couples
# TODO: Diagonal
# TODO: Dutch
# TODO: Even-Odd
# TODO: German
# TODO: Greater Than
# TODO: Jigsaw
# TODO: Killer
# TODO: Kropki
# TODO: Little Unique Killer
# TODO: Lockout Lines
# TODO: Non-Consecutive
# TODO: Quadruple
# TODO: Reflection
# TODO: Renban
# TODO: Running Cells
# TODO: Sandwich
# TODO: Skyscraper
# TODO: Slingshot
# TODO: Slow Thermo
# TODO: Thermo
# TODO: Twisted Consecutive
# TODO: Universal
# TODO: Windoku
# TODO: X-Sum
# TODO: XV
# TODO: Zipper Line
