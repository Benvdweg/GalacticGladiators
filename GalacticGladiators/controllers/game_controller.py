from GalacticGladiators.DAL.unit_dao import UnitDAO
from GalacticGladiators.DAL.game_dao import GameDAO
from GalacticGladiators.DAL.special_powers_log_dao import SpecialPowersLogDAO
from GalacticGladiators.DAL.squares_dao import SquaresDAO
from GalacticGladiators.DAL.square_log_dao import SquareLogDAO
from GalacticGladiators.DAL.game_unit_dao import GameUnitDAO
from GalacticGladiators.ai_player import AiPlayer
from GalacticGladiators.button import Button
from GalacticGladiators.game_service import GameService
from GalacticGladiators.DAL.player_dao import PlayerDAO
import pygame
from GalacticGladiators.cutscene import Cutscene
from GalacticGladiators.human_player import HumanPlayer
from GalacticGladiators.utils.constants import Constants


class GameController:
    def __init__(self, cnx, game_state):
        self.cnx = cnx
        self.game_state = game_state
        self.game_dao = GameDAO(cnx)
        self.squares_dao = SquaresDAO(cnx)
        self.game_unit_dao = GameUnitDAO(cnx)
        self.player_dao = PlayerDAO(cnx)
        self.special_powers_log_dao = SpecialPowersLogDAO(cnx)
        self.unit_dao = UnitDAO(cnx)
        self.square_log_dao = SquareLogDAO(cnx)
        self.game_service = GameService(self.game_dao, self.squares_dao, self.game_unit_dao, self.player_dao,
                                        self.special_powers_log_dao, self.unit_dao, cnx)
        self.buttons = []
        self.game = None
        self.squares = []
        self.squares_map = {}
        self.units_map = {}
        self.player = HumanPlayer(self)
        self.ai_player = AiPlayer(self)

        self.unit_info = {
            1: ("Verkenner", "1"),
            2: ("Infanterist", "2"),
            3: ("Scherpschutter", "3"),
            4: ("Schilddrager", "4"),
            5: ("Strijdmeester", "5"),
            6: ("Commando", "6"),
            7: ("Vlag", "0")
        }

        pygame.mixer.init()

    def create_game(self, nickname):
        return self.game_service.create_game(nickname)

    def get_initial_unit_info(self, game_id):
        unit_types = [1, 2, 3, 4, 5, 6, 7]
        for unit_id in unit_types:
            if self.squares_dao.get_unit_amount_for_player(game_id, unit_id) < self.get_unit_threshold(unit_id):
                return self.get_unit(unit_id)
        return None

    def get_unit_threshold(self, unit_id):
        thresholds = {
            1: 3,
            2: 7,
            3: 3,
            4: 2,
            5: 2,
            6: 2,
            7: 1
        }
        return thresholds.get(unit_id, 0)

    def get_square(self, game_id, col, row):
        return self.squares_dao.get_square(game_id, col, row)

    def get_square_by_id(self, square_id):
        return self.squares_dao.get_square_by_id(square_id)

    def get_game(self, game_id):
        return self.game_dao.get_game(game_id)

    def has_special_power_logs(self, game_unit_id, power_id, is_visible):
        results = self.special_powers_log_dao.get_special_power_logs_for_game_unit(game_unit_id, power_id, is_visible)
        return len(results) > 0

    def get_game_unit(self, square_id):
        return self.game_service.get_game_unit(square_id)

    def get_unit(self, unit_id):
        return self.game_service.get_unit(unit_id)

    def get_unit_by_selected_square_id(self, square_id):
        return self.game_service.get_unit_by_selected_square_id(square_id)

    def show_cutscene(self, screen, game_id):
        player, enemy_player = self.player_dao.get_players(game_id)
        cutscene = Cutscene(screen, player.nickname, enemy_player.nickname, self)
        if not self.game_dao.get_game(game_id).has_ended:
            cutscene.play()
        else:
            if player.score > enemy_player.score:
                name = player.nickname
                player_won = True
            elif player.score < enemy_player.score:
                name = enemy_player.nickname
                player_won = False
            else:
                name = "Niemand"
                player_won = None

            cutscene.play_end_scene(name, f"{player.score} - {enemy_player.score}", player_won)

    def get_players(self, game_id):
        return self.player_dao.get_players(game_id)

    def get_has_ended(self, game_id):
        return self.game_dao.get_game(game_id).has_ended

    def create_button(self, text, start_x, text_y, name, screen):
        button = Button(text, (start_x, text_y), font_size=36, bg_color=(0, 100, 0), text_color=Constants.WHITE,
                        name=name)
        button.draw(screen)
        self.buttons.append(button)

    def add_gold(self, game):
        goldmine_squares = self.squares_dao.get_all_gold_squares(game.game_id)

        for goldmine_square in goldmine_squares:
            if goldmine_square.game_unit:
                self.square_log_dao.add_log(game, goldmine_square)

                logs = self.square_log_dao.get_logs_for_unit_on_square(
                    game.game_id,
                    goldmine_square.game_unit.game_unit_id,
                    goldmine_square.id
                )

                if len(logs) >= 3:
                    last_three_logs = logs[-3:]
                    if (last_three_logs[1].turn_number == last_three_logs[0].turn_number + 1 and
                            last_three_logs[2].turn_number == last_three_logs[1].turn_number + 1):
                        self.player_dao.add_gold(goldmine_square.game_unit.player_id)
                        self.square_log_dao.delete_logs_for_unit_on_square(
                            game.game_id,
                            goldmine_square.game_unit.game_unit_id,
                            goldmine_square.id
                        )
                    else:
                        # Streak is broken, delete all logs
                        self.square_log_dao.delete_logs_for_unit_on_square(
                            game.game_id,
                            goldmine_square.game_unit.game_unit_id,
                            goldmine_square.id
                        )
