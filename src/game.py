from moves import MoveLogic

class Game:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 1
        self.move_logic = MoveLogic(self.board)


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

        if abs(start_row - end_row) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            self.board[middle_row][middle_col] = 0

        return True

    def get_valid_moves_for_player(self):
        capture_moves = self.move_logic.get_all_player_capture_moves(self.current_player)

        if len(capture_moves) > 0:
            return capture_moves

        return self.move_logic.get_all_player_simple_moves(self.current_player)