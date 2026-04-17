from game import Game
from moves import MoveLogic

game = Game()


game.board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

game.move_logic = MoveLogic(game.board)

print("Før første capture:")
game.print_board()
print("Current player:", game.current_player)
print("Valid moves:", game.get_valid_moves_for_player())

game.make_move(5, 0, 3, 2)

print("\nEfter første capture:")
game.print_board()
print("Current player:", game.current_player)
print("must_continue_from:", game.must_continue_from)
print("Valid moves:", game.get_valid_moves_for_player())

game.make_move(3, 2, 1, 4)

print("\nEfter andet capture:")
game.print_board()
print("Current player:", game.current_player)
print("must_continue_from:", game.must_continue_from)

winner = game.check_winner()
print("Vinder:", winner)