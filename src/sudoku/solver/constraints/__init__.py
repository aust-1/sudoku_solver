"""Model classes for Sudoku constraints."""

from src.sudoku.solver.constraints.base_constraint import BaseConstraint
from src.sudoku.solver.constraints.bishop import BishopConstraint
from src.sudoku.solver.constraints.clone import CloneConstraint
from src.sudoku.solver.constraints.clone_zone_constraint import CloneZoneConstraint
from src.sudoku.solver.constraints.even_odd import ParityConstraint
from src.sudoku.solver.constraints.killer import KillerConstraint
from src.sudoku.solver.constraints.king import KingConstraint
from src.sudoku.solver.constraints.knight import KnightConstraint
from src.sudoku.solver.constraints.kropki import KropkiConstraint
from src.sudoku.solver.constraints.palindrome import PalindromeConstraint
from src.sudoku.solver.constraints.universal import UniversalConstraint
from src.sudoku.solver.constraints.xv import XVConstraint

__all__ = [
    "BaseConstraint",
    "BishopConstraint",
    "CloneConstraint",
    "CloneZoneConstraint",
    "KillerConstraint",
    "KingConstraint",
    "KnightConstraint",
    "KropkiConstraint",
    "PalindromeConstraint",
    "ParityConstraint",
    "UniversalConstraint",
    "XVConstraint",
]

# TODO: Arrow
# TODO: Ascending Sequences
# TODO: Between Lines
# TODO: Consecutive
# TODO: Couples
# TODO: Diagonal
# TODO: Dutch
# TODO: German
# TODO: Greater Than
# TODO: Jigsaw
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
# TODO: Windoku
# TODO: X-Sum
# TODO: Zipper Line
