from moves import MoveLogic

class Game:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 1
        self.move_logic = MoveLogic(self.board)
        self.must_continue_from = None

        #Draw regler
        self.position_history = {}
        self.moves_without_capture = 0
        self.draw_available = False
        self.draw_reason = ""

        self.REPETITION_DRAW_LIMIT = 3
        self.no_capture_draw_limit = 1
        #No capture draw limit er "halv-træk" så det skal ses som 40 træk uden
        #capture før at der kan vælges draw, ikke 80.


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

                self.update_draw_rules_after_move(was_capture)

                return True

        self.must_continue_from = None
        self.switch_turn()

        self.update_draw_rules_after_move(was_capture)

        return True

########################################################################################################################

    def get_board_state_key(self):
        """
        Laver en unik nøgle for den nuværende game state.

        Vi gemmer:
        - Boardet
        - Hvis tur det er
        - Om en spiller er tvunget til at fortsætte med samme brik

        På den måde kan vi opdage gentagelser.
        """
        board_tuple = tuple(tuple(row) for row in self.board)
        return (
            board_tuple,
            self.current_player,
            self.must_continue_from
        )

########################################################################################################################

    def register_current_position(self):
        """
        Registrerer den nuværende position i historikken.
        Hvis samme position opstår nok gange, kan spilleren kræve DRAW.
        """

        state_key = self.get_board_state_key()

        if state_key not in self.position_history:
            self.position_history[state_key] = 1
        else:
            self.position_history[state_key] += 1

        if self.position_history[state_key] >= self.REPETITION_DRAW_LIMIT:
            self.draw_available = True
            self.draw_reason = "Samme position opstået 3 gange"

########################################################################################################################

    def update_draw_rules_after_move(self, was_capture):
        """
        Opdaterer draw-reglerne efter hvert træk.
        """

        if was_capture:
            self.moves_without_capture = 0
        else:
            self.moves_without_capture += 1

        if self.moves_without_capture >= self.no_capture_draw_limit:
            self.draw_available = True
            self.draw_reason = "Der er gået for mange træk uden slag"

        self.register_current_position()

########################################################################################################################

    def can_claim_draw(self):
        return self.draw_available

    def claim_draw(self):
        if self.draw_available:
            return "uafgjort"

        return None