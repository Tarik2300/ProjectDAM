from game import Game
from moves import MoveLogic

game = Game()

game.board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

game.move_logic = MoveLogic(game.board)

print("Lovlige moves:")
print(game.get_valid_moves_for_player())

result = game.make_move(6, 1, 5, 0)
print("Move lykkedes:", result)

print("\nBoard efter forsøg:")
game.print_board()