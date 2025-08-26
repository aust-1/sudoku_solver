from enum import Enum, auto


class ConstraintType(Enum):
    """Represents the type of constraint in the Sudoku puzzle."""

    BISHOP = auto()
    CLONE = auto()
    DUTCH = auto()
    EVEN_ODD = auto()
    GERMAN = auto()
    GREATER_THAN = auto()
    KILLER = auto()
    KING = auto()
    KNIGHT = auto()
    KROPKI = auto()
    PALINDROME = auto()
    UNIVERSAL = auto()
    X_V = auto()
    UNDEFINED = auto()
