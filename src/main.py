from game import Game
from ai import AI

game = Game()
ai = AI(2, 3)   # AI spiller som spiller 2 og søger 3 niveauer dybt


def print_board_pretty(board):
    print("   0 1 2 3 4 5 6 7")

    for row_index in range(8):
        print(str(row_index) + "  ", end="")

        for col_index in range(8):
            piece = board[row_index][col_index]

            if piece == 0:
                symbol = "."
            elif piece == 1:
                symbol = "x"
            elif piece == 2:
                symbol = "o"
            elif piece == 3:
                symbol = "X"
            elif piece == 4:
                symbol = "O"

            print(symbol, end=" ")

        print()


def print_moves(moves):
    for i in range(len(moves)):
        start_pos, end_pos = moves[i]
        print(str(i) + ": " + str(start_pos) + " -> " + str(end_pos))


# Hovedloop - kører indtil der findes en vinder eller ingen gyldige moves
while True:
    print()
    print_board_pretty(game.board)
    print()

    winner = game.check_winner()   # tjek om spillet er slut
    if winner is not None:
        print("Vinder:", winner)
        break

    if game.current_player == 1:
        print("Spiller 1 tur")
        print("x = dig, o = AI")
        print("X = din konge, O = AI konge")
        print()

        moves = game.get_valid_moves_for_player()

        if len(moves) == 0:
            print("Ingen gyldige moves")
            break

        print("Gyldige moves:")
        print_moves(moves)

        # Bliver ved med at spørge indtil spilleren vælger et gyldigt move
        while True:
            try:
                choice = int(input("Vælg move nummer: "))

                if choice >= 0 and choice < len(moves):
                    break
                else:
                    print("Ugyldigt nummer. Prøv igen.")

            except:
                print("Skriv et tal.")

        selected_move = moves[choice]

        start_pos, end_pos = selected_move
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        game.make_move(start_row, start_col, end_row, end_col)

    else:
        print("AI tænker...")
        best_move = ai.get_best_move(game)

        if best_move is None:
            print("AI kunne ikke finde et move")
            break

        print("AI valgte:", best_move)

        start_pos, end_pos = best_move
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        game.make_move(start_row, start_col, end_row, end_col)