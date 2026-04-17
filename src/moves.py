class MoveLogic:
    def __init__(self, board):
        self.board = board

########################################################################################################################
    def is_inside_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

########################################################################################################################
    def get_piece_owner(self, piece):
        if piece == 1 or piece == 3:
            return 1
        elif piece == 2 or piece == 4:
            return 2
        return 0
########################################################################################################################
    def is_king(self, piece):
        return piece == 3 or piece == 4

########################################################################################################################
    def get_directions(self, piece):
        if piece == 1:
            return [(-1, -1), (-1, 1)]
        elif piece == 2:
            return [(1, -1),(1, 1)]
        elif piece == 3 or piece == 4:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return []

########################################################################################################################
    def get_simple_moves(self, row, col):
        moves = []
        piece = self.board[row][col]

        if piece == 0:
            return moves

        directions = self.get_directions(piece)

        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col

            if self.is_inside_board(new_row, new_col):
                if self.board[new_row][new_col] == 0:
                    moves.append((new_row, new_col))

        return moves

########################################################################################################################
    def get_capture_moves(self, row, col):
        moves = []
        piece = self.board[row][col]

        if piece == 0:
            return moves

        piece_owner = self.get_piece_owner(piece)
        directions = self.get_directions(piece)

        for d_row, d_col in directions:
            enemy_row = row + d_row
            enemy_col = col + d_col
            landing_row = row + 2 * d_row
            landing_col = col + 2 * d_col

            if self.is_inside_board(enemy_row, enemy_col) and self.is_inside_board(landing_row, landing_col):
                enemy_piece = self.board[enemy_row][enemy_col]
                landing_piece = self.board[landing_row][landing_col]

                if enemy_piece != 0:
                    enemy_owner = self.get_piece_owner(enemy_piece)

                    if enemy_owner != piece_owner and landing_piece == 0:
                        moves.append((landing_row, landing_col))

        return moves


    def get_all_player_simple_moves(self, player):
        all_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if self.get_piece_owner(piece) == player:
                    simple_moves = self.get_simple_moves(row, col)

                    for move in simple_moves:
                        all_moves.append(((row, col), move))

        return all_moves

    def get_all_player_capture_moves(self, player):
        all_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if self.get_piece_owner(piece) == player:
                    capture_moves = self.get_capture_moves(row, col)

                    for move in capture_moves:
                        all_moves = self.get_capture_moves(row, col)

                        for move in capture_moves:
                            all_moves.append(((row, col), move))

        return all_moves