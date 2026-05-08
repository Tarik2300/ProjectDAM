import pygame
import sys

from game import Game
from ai import AI


class PygameUI:
    def __init__(self):
        pygame.init()

        # Layout
        self.BOARD_SIZE = 640
        self.SQUARE_SIZE = self.BOARD_SIZE // 8

        # Plads til koordinater rundt om boardet
        self.BOARD_OFFSET_X = 45
        self.BOARD_OFFSET_Y = 45

        self.SIDE_PANEL_WIDTH = 280

        self.WIDTH = self.BOARD_OFFSET_X + self.BOARD_SIZE + self.SIDE_PANEL_WIDTH
        self.HEIGHT = self.BOARD_OFFSET_Y + self.BOARD_SIZE + 35

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("ProjectDAM - 8-bit Checkers")

        # Farver
        self.BACKGROUND = (18, 18, 18)
        self.PANEL = (28, 28, 36)

        self.LIGHT_SQUARE = (214, 184, 126)
        self.DARK_SQUARE = (92, 58, 38)

        self.WHITE_PIECE = (235, 235, 235)
        self.WHITE_PIECE_DARK = (175, 175, 175)

        self.BLACK_PIECE = (45, 45, 45)
        self.BLACK_PIECE_DARK = (15, 15, 15)

        self.WHITE = (235, 235, 235)
        self.BLACK = (10, 10, 10)
        self.YELLOW = (248, 216, 72)
        self.GREEN = (72, 220, 96)
        self.GREY = (150, 150, 150)

        # Fonts
        self.title_font = pygame.font.SysFont("couriernew", 30, bold=True)
        self.large_font = pygame.font.SysFont("couriernew", 22, bold=True)
        self.normal_font = pygame.font.SysFont("couriernew", 18, bold=True)
        self.small_font = pygame.font.SysFont("couriernew", 15, bold=True)
        self.coord_font = pygame.font.SysFont("couriernew", 18, bold=True)

        # Spil
        self.game = Game()

        # Player 1 = sort og starter altid
        # Player 2 = hvid
        self.human_player = None
        self.ai_player = None
        self.ai = None

        # True indtil spilleren har valgt farve
        self.choosing_color = True

        self.selected_piece = None
        self.valid_moves = []

        self.message = "Vælg sort eller hvid"
        self.game_over = False
        self.winner = None

        self.clock = pygame.time.Clock()

        # Knapper på startskærmen
        self.black_button = pygame.Rect(
            self.WIDTH // 2 - 260,
            self.HEIGHT // 2 + 40,
            220,
            70
        )

        self.white_button = pygame.Rect(
            self.WIDTH // 2 + 40,
            self.HEIGHT // 2 + 40,
            220,
            70
        )

    ####################################################################################################################
    # Hovedloop
    ####################################################################################################################

    def run(self):
        running = True

        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.choosing_color:
                            self.handle_color_selection(event.pos)
                        else:
                            self.handle_mouse_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()

                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if self.choosing_color:
                self.draw_color_selection_screen()
            else:
                self.draw()

        pygame.quit()
        sys.exit()

    ####################################################################################################################
    # Farvevalg
    ####################################################################################################################

    def handle_color_selection(self, mouse_pos):
        if self.black_button.collidepoint(mouse_pos):
            # Brugeren vælger sort.
            # Sort = player 1, og player 1 starter altid.
            self.human_player = 1
            self.ai_player = 2
            self.ai = AI(self.ai_player, 3)

            self.choosing_color = False
            self.message = "Du spiller sort og starter"

            self.auto_select_forced_piece()

        elif self.white_button.collidepoint(mouse_pos):
            # Brugeren vælger hvid.
            # Hvid = player 2.
            # AI bliver derfor sort/player 1 og starter.
            self.human_player = 2
            self.ai_player = 1
            self.ai = AI(self.ai_player, 3)

            self.choosing_color = False
            self.message = "Du spiller hvid - AI starter"

            self.draw()
            pygame.display.update()
            pygame.time.delay(500)

            self.make_ai_move()

    def draw_color_selection_screen(self):
        self.screen.fill(self.BACKGROUND)

        title = self.title_font.render("PROJECT DAM", False, self.YELLOW)
        title_rect = title.get_rect(center=(self.WIDTH // 2, 130))
        self.screen.blit(title, title_rect)

        subtitle = self.large_font.render("VÆLG DIN FARVE", False, self.WHITE)
        subtitle_rect = subtitle.get_rect(center=(self.WIDTH // 2, 190))
        self.screen.blit(subtitle, subtitle_rect)

        info = self.small_font.render("Sort starter altid", False, self.GREY)
        info_rect = info.get_rect(center=(self.WIDTH // 2, 230))
        self.screen.blit(info, info_rect)

        self.draw_selection_button(
            self.black_button,
            "SPIL SORT",
            "Du starter",
            self.BLACK_PIECE,
            self.WHITE
        )

        self.draw_selection_button(
            self.white_button,
            "SPIL HVID",
            "AI starter",
            self.WHITE_PIECE,
            self.BLACK
        )

        pygame.display.update()

    def draw_selection_button(self, rect, title, subtitle, fill_color, text_color):
        pygame.draw.rect(self.screen, self.BLACK, rect.inflate(8, 8))
        pygame.draw.rect(self.screen, fill_color, rect)

        title_surface = self.normal_font.render(title, False, text_color)
        title_rect = title_surface.get_rect(center=(rect.centerx, rect.centery - 12))
        self.screen.blit(title_surface, title_rect)

        subtitle_surface = self.small_font.render(subtitle, False, text_color)
        subtitle_rect = subtitle_surface.get_rect(center=(rect.centerx, rect.centery + 16))
        self.screen.blit(subtitle_surface, subtitle_rect)

    ####################################################################################################################
    # Input
    ####################################################################################################################

    def handle_mouse_click(self, mouse_pos):
        if self.game_over:
            return

        if self.game.current_player != self.human_player:
            return

        self.auto_select_forced_piece()

        board_position = self.get_board_position_from_mouse(mouse_pos)

        if board_position is None:
            return

        row, col = board_position
        clicked_piece = self.game.board[row][col]

        if self.selected_piece is None:
            self.select_piece(row, col)
            return

        start_row, start_col = self.selected_piece
        move_success = self.game.make_move(start_row, start_col, row, col)

        if move_success:
            self.selected_piece = None
            self.valid_moves = []

            winner = self.game.check_winner()
            if winner is not None:
                self.end_game(winner)
                return

            # Hvis spilleren skal fortsætte med samme brik efter slag
            if self.game.current_player == self.human_player and self.game.must_continue_from is not None:
                self.selected_piece = self.game.must_continue_from
                self.update_valid_moves_for_selected_piece()
                self.message = "Du skal slå videre"
                return

            self.message = "AI tænker..."
            self.draw()
            pygame.display.update()

            self.make_ai_move()

        else:
            # Hvis spilleren klikker på en anden af sine egne brikker,
            # kan man vælge den i stedet.
            if self.game.move_logic.get_piece_owner(clicked_piece) == self.human_player:
                self.select_piece(row, col)
            else:
                self.message = "Ugyldigt træk"

    def get_display_position(self, row, col):
        """
        Oversætter intern board-position til visuel position.

        Hvis brugeren spiller hvid, roteres boardet 180 grader,
        så brugerens egne brikker altid vises nederst.
        """

        if self.human_player == 2:
            display_row = 7 - row
            display_col = 7 - col
        else:
            display_row = row
            display_col = col

        return display_row, display_col

    def get_board_position_from_mouse(self, mouse_pos):
        """
        Oversætter museklik på det viste board til intern board-position.

        Når boardet er roteret, skal klik også vendes om,
        så Game stadig får de rigtige row/col-værdier.
        """

        mouse_x, mouse_y = mouse_pos

        board_left = self.BOARD_OFFSET_X
        board_top = self.BOARD_OFFSET_Y
        board_right = self.BOARD_OFFSET_X + self.BOARD_SIZE
        board_bottom = self.BOARD_OFFSET_Y + self.BOARD_SIZE

        if mouse_x < board_left or mouse_x >= board_right:
            return None

        if mouse_y < board_top or mouse_y >= board_bottom:
            return None

        display_col = (mouse_x - self.BOARD_OFFSET_X) // self.SQUARE_SIZE
        display_row = (mouse_y - self.BOARD_OFFSET_Y) // self.SQUARE_SIZE

        if self.human_player == 2:
            row = 7 - display_row
            col = 7 - display_col
        else:
            row = display_row
            col = display_col

        return row, col

    def select_piece(self, row, col):
        piece = self.game.board[row][col]

        if self.game.move_logic.get_piece_owner(piece) != self.human_player:
            self.message = "Vælg en af dine brikker"
            return

        all_valid_moves = self.game.get_valid_moves_for_player()

        piece_has_valid_move = False

        for move in all_valid_moves:
            start_pos, end_pos = move

            if start_pos == (row, col):
                piece_has_valid_move = True
                break

        if not piece_has_valid_move:
            self.message = "Den brik kan ikke flytte"
            return

        self.selected_piece = (row, col)
        self.update_valid_moves_for_selected_piece()
        self.message = "Vælg et grønt felt"

    def update_valid_moves_for_selected_piece(self):
        self.valid_moves = []

        if self.selected_piece is None:
            return

        all_valid_moves = self.game.get_valid_moves_for_player()
        selected_row, selected_col = self.selected_piece

        for move in all_valid_moves:
            start_pos, end_pos = move

            if start_pos == (selected_row, selected_col):
                self.valid_moves.append(end_pos)

    ####################################################################################################################
    # Tvungen slagmarkering
    ####################################################################################################################

    def auto_select_forced_piece(self):
        """
        Hvis spilleren kun har én brik, der lovligt må bruges pga. slag,
        markerer UI'et automatisk den brik og dens mulige felter.
        """

        if self.game_over:
            return

        if self.human_player is None:
            return

        if self.game.current_player != self.human_player:
            return

        all_valid_moves = self.game.get_valid_moves_for_player()

        if len(all_valid_moves) == 0:
            return

        capture_moves = []

        for move in all_valid_moves:
            start_pos, end_pos = move
            start_row, start_col = start_pos
            end_row, end_col = end_pos

            if abs(start_row - end_row) == 2:
                capture_moves.append(move)

        # Hvis der ikke er slagtræk, skal UI'et ikke autovælge
        if len(capture_moves) == 0:
            return

        forced_start_positions = []

        for move in capture_moves:
            start_pos, end_pos = move

            if start_pos not in forced_start_positions:
                forced_start_positions.append(start_pos)

        # Kun hvis præcis én brik er lovlig
        if len(forced_start_positions) == 1:
            self.selected_piece = forced_start_positions[0]
            self.update_valid_moves_for_selected_piece()
            self.message = "Tvunget slag - brug markeret brik"

    ####################################################################################################################
    # AI
    ####################################################################################################################

    def make_ai_move(self):
        if self.game_over:
            return

        if self.ai is None:
            return

        if self.game.current_player != self.ai_player:
            return

        pygame.time.delay(500)

        while self.game.current_player == self.ai_player and not self.game_over:
            best_move = self.ai.get_best_move(self.game)

            if best_move is None:
                self.end_game(self.human_player)
                return

            start_pos, end_pos = best_move
            start_row, start_col = start_pos
            end_row, end_col = end_pos

            self.game.make_move(start_row, start_col, end_row, end_col)

            winner = self.game.check_winner()
            if winner is not None:
                self.end_game(winner)
                return

            # Hvis AI skal slå videre, bliver current_player stadig AI
            if self.game.current_player == self.ai_player:
                pygame.time.delay(400)
                self.draw()
                pygame.display.update()

        self.message = "Din tur"
        self.auto_select_forced_piece()

    ####################################################################################################################
    # Tegning
    ####################################################################################################################

    def draw(self):
        self.screen.fill(self.BACKGROUND)

        self.draw_coordinates()
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        self.draw_side_panel()

        pygame.display.update()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                display_row, display_col = self.get_display_position(row, col)

                x = self.BOARD_OFFSET_X + display_col * self.SQUARE_SIZE
                y = self.BOARD_OFFSET_Y + display_row * self.SQUARE_SIZE

                if (row + col) % 2 == 0:
                    color = self.LIGHT_SQUARE
                else:
                    color = self.DARK_SQUARE

                pygame.draw.rect(
                    self.screen,
                    color,
                    (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                )

                pygame.draw.rect(
                    self.screen,
                    self.BLACK,
                    (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE),
                    2
                )

    def draw_coordinates(self):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]

        # Bogstaver under boardet
        for display_col in range(8):
            if self.human_player == 2:
                board_col = 7 - display_col
            else:
                board_col = display_col

            letter = letters[board_col]

            text = self.coord_font.render(letter, False, self.WHITE)
            text_rect = text.get_rect()

            x = self.BOARD_OFFSET_X + display_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 - text_rect.width // 2
            y = self.BOARD_OFFSET_Y + self.BOARD_SIZE + 8

            self.screen.blit(text, (x, y))

        # Tal til venstre for boardet
        for display_row in range(8):
            if self.human_player == 2:
                board_row = 7 - display_row
            else:
                board_row = display_row

            number = numbers[board_row]

            text = self.coord_font.render(number, False, self.WHITE)
            text_rect = text.get_rect()

            x = self.BOARD_OFFSET_X - 28
            y = self.BOARD_OFFSET_Y + display_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 - text_rect.height // 2

            self.screen.blit(text, (x, y))

    def draw_highlights(self):
        # Marker valgt/tvungen brik
        if self.selected_piece is not None:
            row, col = self.selected_piece

            display_row, display_col = self.get_display_position(row, col)

            x = self.BOARD_OFFSET_X + display_col * self.SQUARE_SIZE
            y = self.BOARD_OFFSET_Y + display_row * self.SQUARE_SIZE

            pygame.draw.rect(
                self.screen,
                self.YELLOW,
                (x + 4, y + 4, self.SQUARE_SIZE - 8, self.SQUARE_SIZE - 8),
                6
            )

        # Marker gyldige felter
        for move in self.valid_moves:
            row, col = move

            display_row, display_col = self.get_display_position(row, col)

            x = self.BOARD_OFFSET_X + display_col * self.SQUARE_SIZE
            y = self.BOARD_OFFSET_Y + display_row * self.SQUARE_SIZE

            marker_size = 24
            marker_x = x + self.SQUARE_SIZE // 2 - marker_size // 2
            marker_y = y + self.SQUARE_SIZE // 2 - marker_size // 2

            pygame.draw.rect(
                self.screen,
                self.GREEN,
                (marker_x, marker_y, marker_size, marker_size)
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                (marker_x, marker_y, marker_size, marker_size),
                3
            )

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]

                if piece != 0:
                    self.draw_piece(row, col, piece)

    def draw_piece(self, row, col, piece):
        display_row, display_col = self.get_display_position(row, col)

        x = self.BOARD_OFFSET_X + display_col * self.SQUARE_SIZE
        y = self.BOARD_OFFSET_Y + display_row * self.SQUARE_SIZE

        piece_margin = 14
        piece_size = self.SQUARE_SIZE - piece_margin * 2

        piece_x = x + piece_margin
        piece_y = y + piece_margin

        # Player 1 = sort
        # Player 2 = hvid
        if piece == 1 or piece == 3:
            main_color = self.BLACK_PIECE
            shadow_color = self.BLACK_PIECE_DARK
            text_color = self.WHITE
        else:
            main_color = self.WHITE_PIECE
            shadow_color = self.WHITE_PIECE_DARK
            text_color = self.BLACK

        # Sort kant
        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (piece_x - 4, piece_y - 4, piece_size + 8, piece_size + 8)
        )

        # Mørk skygge
        pygame.draw.rect(
            self.screen,
            shadow_color,
            (piece_x, piece_y + 6, piece_size, piece_size)
        )

        # Hovedform
        pygame.draw.rect(
            self.screen,
            main_color,
            (piece_x, piece_y, piece_size, piece_size)
        )

        # Skær hjørner væk for pixel/8-bit form
        corner_size = 10

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (piece_x, piece_y, corner_size, corner_size)
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (piece_x + piece_size - corner_size, piece_y, corner_size, corner_size)
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (piece_x, piece_y + piece_size - corner_size, corner_size, corner_size)
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (piece_x + piece_size - corner_size, piece_y + piece_size - corner_size, corner_size, corner_size)
        )

        # Lille pixel-highlight
        pygame.draw.rect(
            self.screen,
            self.WHITE,
            (piece_x + 10, piece_y + 10, 12, 12)
        )

        # Konge
        if piece == 3 or piece == 4:
            king_text = self.large_font.render("K", False, text_color)
            king_rect = king_text.get_rect(
                center=(
                    x + self.SQUARE_SIZE // 2,
                    y + self.SQUARE_SIZE // 2
                )
            )
            self.screen.blit(king_text, king_rect)

    ####################################################################################################################
    # Sidepanel
    ####################################################################################################################

    def draw_side_panel(self):
        panel_x = self.BOARD_OFFSET_X + self.BOARD_SIZE

        pygame.draw.rect(
            self.screen,
            self.PANEL,
            (panel_x, 0, self.SIDE_PANEL_WIDTH, self.HEIGHT)
        )

        # Pixel-kant mellem board og panel
        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (panel_x, 0, 5, self.HEIGHT)
        )

        title = self.title_font.render("PROJECT", False, self.WHITE)
        self.screen.blit(title, (panel_x + 25, 35))

        title_2 = self.title_font.render("DAM", False, self.YELLOW)
        self.screen.blit(title_2, (panel_x + 25, 68))

        self.draw_turn_info(panel_x)
        self.draw_piece_count(panel_x)
        self.draw_help_text(panel_x)

        if self.game_over:
            self.draw_game_over(panel_x)

    def draw_turn_info(self, panel_x):
        y = 135

        title = self.large_font.render("STATUS", False, self.WHITE)
        self.screen.blit(title, (panel_x + 25, y))

        y += 35

        if self.game.current_player == self.human_player:
            turn_text = "TUR: DIG"
            color = self.YELLOW
        else:
            turn_text = "TUR: AI"
            color = self.GREY

        turn_surface = self.normal_font.render(turn_text, False, color)
        self.screen.blit(turn_surface, (panel_x + 25, y))

        y += 35

        wrapped_lines = self.wrap_text(self.message, 230)

        for line in wrapped_lines:
            line_surface = self.small_font.render(line, False, self.WHITE)
            self.screen.blit(line_surface, (panel_x + 25, y))
            y += 22

    def draw_piece_count(self, panel_x):
        y = 270

        title = self.large_font.render("BRIKKER", False, self.WHITE)
        self.screen.blit(title, (panel_x + 25, y))

        y += 38

        black_pieces = self.game.count_player_pieces(1)
        white_pieces = self.game.count_player_pieces(2)

        black_text = self.normal_font.render("SORT: " + str(black_pieces), False, self.GREY)
        white_text = self.normal_font.render("HVID: " + str(white_pieces), False, self.WHITE_PIECE)

        self.screen.blit(black_text, (panel_x + 25, y))
        self.screen.blit(white_text, (panel_x + 25, y + 28))

        y += 70

        if self.human_player == 1:
            player_text = "DU: SORT"
        elif self.human_player == 2:
            player_text = "DU: HVID"
        else:
            player_text = "DU: -"

        player_surface = self.small_font.render(player_text, False, self.YELLOW)
        self.screen.blit(player_surface, (panel_x + 25, y))

    def draw_help_text(self, panel_x):
        y = 410

        title = self.large_font.render("KONTROL", False, self.WHITE)
        self.screen.blit(title, (panel_x + 25, y))

        help_lines = [
            "Klik brik",
            "Klik grønt felt",
            "R   = genstart",
            "ESC = luk",
            "",
            "Sort starter",
            "K = konge"
        ]

        y += 38

        for line in help_lines:
            text_surface = self.small_font.render(line, False, self.WHITE)
            self.screen.blit(text_surface, (panel_x + 25, y))
            y += 23

    def draw_game_over(self, panel_x):
        y = 610

        if self.winner == "Uafgjort":
            text = "UAFGJORT"
        elif self.winner == self.human_player:
            text = "DU VANDT"
        elif self.winner == self.ai_player:
            text = "AI VANDT"
        else:
            text = "SPIL SLUT"

        game_over_surface = self.large_font.render(text, False, self.YELLOW)
        self.screen.blit(game_over_surface, (panel_x + 25, y))

        restart_surface = self.small_font.render("Tryk R for nyt spil", False, self.WHITE)
        self.screen.blit(restart_surface, (panel_x + 25, y + 35))

    ####################################################################################################################
    # Hjælpemetoder
    ####################################################################################################################

    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = self.small_font.render(test_line, False, self.WHITE)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line != "":
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line != "":
            lines.append(current_line.strip())

        return lines

    def end_game(self, winner):
        self.game_over = True
        self.winner = winner

        if winner == "Uafgjort":
            self.message = "Spillet endte uafgjort"
        elif winner == self.human_player:
            self.message = "Du har vundet"
        elif winner == self.ai_player:
            self.message = "AI har vundet"

    def restart_game(self):
        self.game = Game()

        self.human_player = None
        self.ai_player = None
        self.ai = None

        self.choosing_color = True

        self.selected_piece = None
        self.valid_moves = []

        self.message = "Vælg sort eller hvid"
        self.game_over = False
        self.winner = None