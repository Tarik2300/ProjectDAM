import copy


class AI:
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth

    # Simpel evalueringsfunktion:
    # spiller 2 er positiv, spiller 1 er negativ
    # konge tæller dobbelt
    def evaluate(self, game):
        score = 0

        for row in game.board:
            for piece in row:
                if piece == 1:
                    score -= 1
                elif piece == 2:
                    score += 1
                elif piece == 3:
                    score -= 2
                elif piece == 4:
                    score += 2

        return score

    def get_copy_of_game(self, game):
        return copy.deepcopy(game)

    # Laver et move på en kopi af spillet, så det rigtige board ikke ændres
    def try_move(self, game, move):
        new_game = self.get_copy_of_game(game)

        start_pos, end_pos = move
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        new_game.make_move(start_row, start_col, end_row, end_col)
        return new_game

    # Minimax med alpha-beta pruning
    def minimax(self, game, depth, alpha, beta, maximizing):
        winner = game.check_winner()

        if winner == 2:
            return 1000, None
        elif winner == 1:
            return -1000, None
        elif winner == "Uafgjort":
            return 0, None

        if depth == 0:
            return self.evaluate(game), None

        moves = game.get_valid_moves_for_player()

        if len(moves) == 0:
            return self.evaluate(game), None

        best_move = None

        if maximizing:
            best_score = -9999

            for move in moves:
                new_game = self.try_move(game, move)
                score, _ = self.minimax(new_game, depth - 1, alpha, beta, False)

                if score > best_score:
                    best_score = score
                    best_move = move

                if score > alpha:
                    alpha = score

                if beta <= alpha:
                    break

            return best_score, best_move

        else:
            best_score = 9999

            for move in moves:
                new_game = self.try_move(game, move)
                score, _ = self.minimax(new_game, depth - 1, alpha, beta, True)

                if score < best_score:
                    best_score = score
                    best_move = move

                if score < beta:
                    beta = score

                if beta <= alpha:
                    break

            return best_score, best_move

    def get_best_move(self, game):
        score, move = self.minimax(game, self.depth, -9999, 9999, True)
        return move