from moves import MoveLogic

class Game:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 1
        self.move_logic = MoveLogic(self.board)
        self.must_continue_from = None


    #Selve boardet er på en række lister
    #tallet "1" er den ene spillers brikker og 2 er modstanderens.
    #tallene 0 er tomme felter
    #Fordi det er muligt at få en "konge" i dam, kommer kongen til at være "3" og "4", alt afhængigt af spiller
    def create_board(self):
        return [
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
    ]

    #Initialiserer board
    def print_board(self):
        for row in self.board:
            print(row)

########################################################################################################################
    #Kroning
    def crown_piece(self, row, col):
        piece = self.board[row][col]

        if piece == 1 and row == 0:
            self.board[row][col] = 3
        elif piece == 2 and row == 7:
            self.board[row][col] = 4

########################################################################################################################

    def get_valid_moves_for_player(self):
        if self.must_continue_from is not None:
            row, col = self.must_continue_from
            capture_moves = self.move_logic.get_capture_moves(row, col)

            forced_moves = []
            for move in capture_moves:
                forced_moves.append(((row, col), move))

            return forced_moves

        capture_moves = self.move_logic.get_all_player_capture_moves(self.current_player)

        if len(capture_moves) > 0:
            return capture_moves

        return self.move_logic.get_all_player_simple_moves(self.current_player)

########################################################################################################################

    def switch_turn(self):
        self.must_continue_from = None

        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

########################################################################################################################

    def count_player_pieces(self, player):
        count = 0

        for row in self.board:
            for piece in row:
                if self.move_logic.get_piece_owner(piece) == player:
                    count += 1

        return count

########################################################################################################################

    def check_winner(self):
        player_1_pieces = self.count_player_pieces(1)
        player_2_pieces = self.count_player_pieces(2)

        if player_1_pieces == 0 and player_2_pieces == 0:
            return "Uafgjort"

        if player_1_pieces == 0:
            return 2
        if player_2_pieces == 0:
            return 1

        current_moves = self.get_valid_moves_for_player()

        if len(current_moves) == 0:
            if self.current_player == 1:
                return 2
            else:
                return 1

        return None

########################################################################################################################

    def make_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]

        if self.move_logic.get_piece_owner(piece) != self.current_player:
            print("Det er ikke din brik")
            return False

        valid_moves = self.get_valid_moves_for_player()
        chosen_move = ((start_row, start_col), (end_row, end_col))

        if chosen_move not in valid_moves:
            print("Ugyldigt move")
            return False

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = 0

        was_capture = abs(start_row - end_row) == 2

        if was_capture:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            self.board[middle_row][middle_col] = 0

        self.crown_piece(end_row, end_col)

        if was_capture:
            more_captures = self.move_logic.get_capture_moves(end_row, end_col)

            if len(more_captures) > 0:
                self.must_continue_from = (end_row, end_col)
                return True

        self.switch_turn()
        return True