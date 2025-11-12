import pygame
from DAL.squares_dao import SquaresDAO
from DAL.game_unit_dao import GameUnitDAO
from unit import Scout, Infantry, Sniper, ShieldBearer, BattleMaster, Commando, Flag
from utils.constants import Constants


class GameBoard:
    def __init__(self, screen, game_id, cnx, game_controller, player, enemy_player, cheatcode):
        self.screen = screen
        self.cnx = cnx
        self.game_controller = game_controller
        self.game = self.game_controller.get_game(game_id)
        self.player = player
        self.enemy_player = enemy_player
        self.square_dao = SquaresDAO(cnx)
        self.cheatcode = cheatcode
        self.game_unit_dao = GameUnitDAO(cnx)

        self.colors = {
            "elevated": Constants.BLUE,
            "coverage": Constants.PURPLE,
            "sensor": Constants.RED,
            "goldmine": Constants.YELLOW
        }

        self.small_font = pygame.font.Font(None, 14)
        self.medium_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)

    def draw_text(self, text, position, font_size=36, color=Constants.BLACK):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw(self):
        self.screen.fill(Constants.DEFAULT_INNER_COLOR)

        self.draw_text(self.player.nickname, (10, 10))

        self.draw_captured_enemies()
        self.draw_board(5, 100)
        self.draw_units()
        self.draw_labels()
        self.draw_unit_info()

        board_height = Constants.GRID_SIZE * 80
        self.draw_text(self.enemy_player.nickname, (10, board_height + 110))
        self.draw_captured_friendly_units(board_height)

    def draw_captured_units(self, units, start_x, start_y, color):
        circle_radius = 18
        spacing_x = 40

        for i, unit in enumerate(units):
            x = start_x + i * spacing_x
            y = start_y

            pygame.draw.circle(self.screen, color, (x, y), circle_radius)

            text = str(unit.rank) if unit.captured_at_turn == self.game.current_turn - 1 or self.cheatcode or self.game.has_ended else ""

            if text:
                text_surface = self.medium_font.render(text, True, Constants.WHITE)
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)

    def draw_captured_enemies(self):
        captured_enemies = self.game_unit_dao.get_captured_enemies(self.game.game_id)
        self.draw_captured_units(captured_enemies, 20, 60, Constants.ENEMY_BLUE)

    def draw_captured_friendly_units(self, board_height):
        captured_units = self.game_unit_dao.get_captured_from_player(self.game.game_id)
        self.draw_captured_units(captured_units, 20, board_height + 160, Constants.ORANGE)

    def draw_board(self, start_x, start_y):
        self.game_controller.squares = []
        self.game_controller.squares_map = {}

        for row in range(Constants.GRID_SIZE):
            for col in range(Constants.GRID_SIZE):
                self.draw_square(col, row, start_x, start_y)

    def draw_square(self, col, row, start_x, start_y):
        current_square = self.game_controller.get_square(self.game.game_id, col + 1, row + 1)
        selected_square = self.game_controller.get_square_by_id(self.game.selected_unit_square_id)

        inner_color = self.colors.get(current_square.square_type, Constants.DEFAULT_INNER_COLOR)
        if selected_square and self.is_adjacent(selected_square, current_square):
            unit = self.game_controller.get_unit_by_selected_square_id(selected_square.id)
            if unit and unit.unit_id != 7 and (not current_square.game_unit and not self.game.has_ended):
                inner_color = Constants.GREEN

        if selected_square and self.is_adjacent(selected_square, current_square) and current_square.unit_id and not current_square.game_unit.is_friendly:
            inner_color = Constants.ATTACK_COLOR

        rect = pygame.Rect(start_x + col * 80, start_y + row * 80, 80, 80)
        self.game_controller.squares.append((rect, current_square))
        self.game_controller.squares_map[(rect.x, rect.y)] = current_square

        pygame.draw.rect(self.screen, inner_color, rect)
        pygame.draw.rect(self.screen, Constants.BORDER_COLOR, rect, 1)

        if current_square.unit_id and not current_square.game_unit.is_friendly:
            self.draw_enemy_unit(rect, current_square)

    @staticmethod
    def is_adjacent(selected_square, current_square):
        return (abs(current_square.x - selected_square.x) == 1 and current_square.y == selected_square.y) or \
            (abs(current_square.y - selected_square.y) == 1 and current_square.x == selected_square.x)

    def draw_enemy_unit(self, rect, current_square):
        if not self.game_controller.has_special_power_logs(current_square.unit_id, 1, False):
            pygame.draw.circle(self.screen, Constants.ENEMY_BLUE, rect.center, 30)

        if current_square.square_type == "sensor":
            unit_name = Constants.UNIT_NAMES.get(current_square.game_unit.unit_id, "Unknown")
            text_surface = self.small_font.render(unit_name, True, Constants.WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        if self.cheatcode or self.game.has_ended or self.game_controller.has_special_power_logs(current_square.unit_id, 4, True):
            rank = current_square.game_unit.rank + 1 if current_square.square_type == "elevated" else current_square.game_unit.rank
            self.draw_unit_rank(rect.center, str(rank), self.game_controller.has_special_power_logs(current_square.unit_id, 4, True))

    def draw_units(self):
        for rect, current_square in self.game_controller.squares:
            if current_square.game_unit:
                if current_square.game_unit.is_friendly and not current_square.game_unit.is_defeated:
                    if self.game_controller.has_special_power_logs(current_square.unit_id, 1, False):
                        pygame.draw.circle(self.screen, (255, 200, 100), rect.center, 20)
                    elif self.game_controller.has_special_power_logs(current_square.unit_id, 4, False):
                        pygame.draw.circle(self.screen, (200, 100, 0), rect.center, 20)
                    else:
                        pygame.draw.circle(self.screen, (255, 165, 0), rect.center, 20)

                    if current_square.game_unit.unit_id == 1:
                        unit = Scout(self.cnx, self.game)
                    elif current_square.game_unit.unit_id == 2:
                        unit = Infantry(self.cnx, self.game)
                    elif current_square.game_unit.unit_id == 3:
                        unit = Sniper(self.cnx, self.game)
                    elif current_square.game_unit.unit_id == 4:
                        unit = ShieldBearer(self.cnx, self.game)
                    elif current_square.game_unit.unit_id == 5:
                        unit = BattleMaster(self.cnx, self.game)
                    elif current_square.game_unit.unit_id == 6:
                        unit = Commando(self.cnx, self.game)
                    else:
                        unit = Flag(self.cnx, self.game)

                    self.game_controller.units_map[current_square.game_unit.game_unit_id] = unit

                    rank = self.square_dao.get_game_unit_rank(current_square.id)

                    rank = rank + 1 if current_square.square_type == "elevated" else rank

                    self.draw_unit_rank(rect.center, str(rank), self.game_controller.has_special_power_logs(current_square.unit_id, 4, True))

    def draw_unit_rank(self, center, rank, is_revealed):
        if is_revealed:
            text_color = Constants.RED
        else:
            text_color = Constants.WHITE

        text_surface = self.medium_font.render(rank, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    def draw_labels(self):
        square_size = 70
        space_between_squares = 30
        start_x = Constants.GRID_SIZE * square_size + 130
        start_y = 20

        for i, label in enumerate(Constants.FIELD_TYPES):
            y_position = start_y + i * (square_size + space_between_squares)
            self.draw_single_label(label, start_x, y_position, square_size)

    def draw_single_label(self, label, start_x, y_position, square_size):
        pygame.draw.rect(self.screen, self.colors[label],
                         pygame.Rect(start_x, y_position + 20, square_size, square_size))
        text_surface = self.large_font.render(label, True, Constants.BLACK)
        text_x = start_x + square_size + 10
        text_y = y_position + (square_size - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

    def draw_unit_info(self):
        if not self.game.has_started:
            unit = self.game_controller.get_initial_unit_info(self.game.game_id)
        else:
            unit = self.game_controller.get_unit_by_selected_square_id(self.game.selected_unit_square_id)

        if unit and not self.game.has_ended:
            unit_name = unit.type
            if unit.unit_id == 7:
                unit_rank = "0"
            else:
                unit_rank = str(unit.unit_id)
        else:
            unit_name = ""
            unit_rank = ""

        start_x, text_y, text_name_height = self.draw_selected_unit_info(unit_name, unit_rank)

        player, enemy_player = self.game_controller.get_players(self.game.game_id)

        self.game_controller.create_button("Hoofdmenu", start_x, text_y + text_name_height + 105, "main_menu", self.screen)

        if not self.game.has_started and not unit_name:
            self.game_controller.create_button("Start Game", start_x, text_y + text_name_height + 50, "start_game", self.screen)
        elif self.game.has_ended:
            text_gold = self.large_font.render(f"Jouw schatkist: {player.score} dukaten", True, Constants.BLACK)
            start_x = Constants.GRID_SIZE * 80 + 30
            text_y = 570 + text_name_height - 120
            self.screen.blit(text_gold, (start_x, text_y))

            text_gold = self.large_font.render(f"De schatkist van de tegenstander: {enemy_player.score} dukaten", True, Constants.BLACK)
            text_y = 570 + text_name_height + 250
            self.screen.blit(text_gold, (start_x, text_y))
        elif self.game.has_started and unit_name:
            game_unit = self.game_controller.get_game_unit(self.game.selected_unit_square_id)
            if game_unit and unit.special_power != "Geen" and not game_unit.has_used_power:
                self.game_controller.create_button(unit.special_power, start_x, text_y + text_name_height + 50, "special_power", self.screen)

    def draw_selected_unit_info(self, unit_name, unit_rank):
        if unit_name == "":
            return 830, 614, 24
        self.game_controller.buttons = []
        start_x = Constants.GRID_SIZE * 80 + 30
        text_y = 570
        text_name = self.large_font.render(f"Geselecteerd: {unit_name}", True, Constants.BLACK)
        text_rank = self.large_font.render(f"Rank: {unit_rank}", True, Constants.BLACK)
        text_y += 10
        self.screen.blit(text_name, (start_x, text_y))
        text_y += text_name.get_height() + 10
        self.screen.blit(text_rank, (start_x, text_y))
        return start_x, text_y, text_name.get_height()
