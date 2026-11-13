from models import Board
from solver.constraints.clone_zone_constraint import CloneZoneConstraint
from solver.constraints.structs import ConstraintType


def make_constraint(board: Board) -> CloneZoneConstraint:
    zone_a = [board.get_cell(pos="a1"), board.get_cell(pos="a2")]
    zone_b = [board.get_cell(pos="e5"), board.get_cell(pos="e6")]
    return CloneZoneConstraint(zone_a, zone_b)


class TestCloneZoneConstraintSerialization:
    def test_type_is_clone_zone(self) -> None:
        board = Board(9)

        assert make_constraint(board).type == ConstraintType.CLONE_ZONE

    def test_to_dict_uses_clone_zone_type(self) -> None:
        board = Board(9)

        assert make_constraint(board).to_dict()["type"] == "clone_zone"

    def test_board_round_trip_reloads_clone_zone(self) -> None:
        board = Board(9)
        board.add_constraints(make_constraint(board))

        reloaded = Board.from_dict(board.to_dict())

        assert [type(c) for c in reloaded.constraints] == [CloneZoneConstraint]
