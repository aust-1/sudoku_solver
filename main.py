from common import Board


game_board = Board()

print("Initial Board:")
print(game_board)
print("Is the board full?", game_board.is_full())
print("Adding piece '5' at (0, 0):", game_board.add_piece(0, 0, 5))
print("Board after adding piece:")
print(game_board)
