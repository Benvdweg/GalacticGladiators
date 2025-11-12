import random
import logging
from utils.constants import Constants
from decorators import power_expiration_check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_grid_squares(squares_dao, game_id):
    for x in range(1, Constants.GRID_SIZE + 1):
        for y in range(1, Constants.GRID_SIZE + 1):
            squares_dao.create_square(game_id, x, y)


class GameService:
    def __init__(self, game_dao, squares_dao, game_unit_dao, player_dao, special_powers_log_dao, unit_dao, cnx):
        self.game_dao = game_dao
        self.squares_dao = squares_dao
        self.game_unit_dao = game_unit_dao
        self.player_dao = player_dao
        self.special_powers_log_dao = special_powers_log_dao
        self.unit_dao = unit_dao
        self.cnx = cnx

    def create_game(self, nickname):
        game_id = self.game_dao.create_game()

        enemy_id = self.player_dao.create_players_for_game(nickname, game_id)
        self._create_grid_squares(game_id)
        self._place_special_fields(game_id)
        self._place_enemy_units(game_id, enemy_id)
        return game_id

    def _create_grid_squares(self, game_id):
        create_grid_squares(self.squares_dao, game_id)

    def _place_special_fields(self, game_id):
        random_positions = random.sample(Constants.SPECIAL_FIELD_POSITIONS, sum(Constants.FIELD_COUNTS.values()))
        for field_type in Constants.FIELD_TYPES:
            self._place_fields(random_positions, field_type, Constants.FIELD_COUNTS[field_type], game_id)

    def _place_fields(self, random_positions, field_type, count, game_id):
        positions = random.sample(random_positions, count)
        for pos in positions:
            random_positions.remove(pos)
            self.squares_dao.place_special_field(game_id, pos[1], pos[0], field_type)

    def _place_enemy_units(self, game_id, enemy_id):
        enemy_units_positions = Constants.ENEMY_UNIT_POSITIONS[:]
        for unit_id, count in Constants.UNIT_COUNTS.items():
            for _ in range(count):
                pos = random.choice(enemy_units_positions)
                enemy_units_positions.remove(pos)
                game_unit_id = self.game_unit_dao.create_game_unit(enemy_id, unit_id, game_id, False)
                self.squares_dao.place_enemy_unit(game_id, pos[1], pos[0], game_unit_id)

    def calculate_score(self, game, bot_won):
        self.game_dao.end_game(game.game_id)
        self.player_dao.update_score(10, game.game_id, bot_won)

        game_units = self.game_unit_dao.get_all_game_units(game.game_id)

        for game_unit in game_units:
            if not game_unit.is_defeated:
                self.player_dao.update_score(1, game.game_id, not game_unit.is_friendly)

    def undo_powers(self, game):
        all_powers = self.special_powers_log_dao.get_all_special_powers_log(game.game_id)

        for power in all_powers:
            if power.power == 1 or (power.power == 4 and not power.is_visible):
                self._undo_invisibility(game, power)
            elif power.power == 5:
                self._undo_rank_up(game, power)

    @power_expiration_check(3)
    def _undo_invisibility(self, game, power):
        return True

    @power_expiration_check(1)
    def _undo_rank_up(self, game, power):
        self.game_unit_dao.update_rank(power.game_unit_id, -1)
        return True

    def get_unit_by_selected_square_id(self, square_id):
        game_unit = self.get_game_unit(square_id)
        if game_unit:
            return self.get_unit(game_unit.unit_id)
        return None

    def get_game_unit(self, square_id):
        return self.game_unit_dao.get_game_unit(square_id)

    def get_unit(self, unit_id):
        return self.unit_dao.get_unit(unit_id)
