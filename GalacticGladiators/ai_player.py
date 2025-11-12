import random

from GalacticGladiators.game_service import logger
from GalacticGladiators.player import Player
from GalacticGladiators.unit import Commando, Scout, Sniper, BattleMaster, ShieldBearer
from GalacticGladiators.utils.constants import Constants


class AiPlayer(Player):
    def __init__(self, game_controller):
        super().__init__(game_controller)

    def move_random_enemy_unit(self, game_id, game):
        enemy_squares = self.game_controller.squares_dao.get_all_active_enemy_units(game_id)
        if not enemy_squares:
            return

        random.shuffle(enemy_squares)
        for selected_enemy_square in enemy_squares:
            if self._can_sabotage(selected_enemy_square, game):
                return

        for selected_enemy_square in enemy_squares:
            if self._attempt_use_enemy_power(selected_enemy_square, game):
                return

            if self._attempt_move_enemy_unit(selected_enemy_square, game):
                return

        logger.warning("No enemy units could move this turn.")

    def _attempt_move_enemy_unit(self, selected_enemy_square, game):
        valid_positions = self._get_valid_positions(selected_enemy_square.x, selected_enemy_square.y, game.game_id)
        random.shuffle(valid_positions)
        for new_position in valid_positions:
            if self.game_controller.squares_dao.is_position_valid(game.game_id, new_position[0], new_position[1]):
                target_square = self.game_controller.squares_dao.get_square(game.game_id, new_position[0],
                                                                            new_position[1])

                if target_square.game_unit:
                    is_invisible = self.game_controller.special_powers_log_dao.get_special_power_logs_for_game_unit(
                        target_square.game_unit.
                        game_unit_id, 1, False)

                    if is_invisible:
                        self.game_controller.game_unit_dao.defeat_unit(selected_enemy_square.game_unit.game_unit_id,
                                                                       game.game_id)
                        self.game_controller.squares_dao.update_square_units_by_id(
                            selected_enemy_square.game_unit.game_unit_id)
                    else:
                        self.handle_attack(selected_enemy_square, target_square, game)
                else:
                    self.game_controller.squares_dao.update_square_units(game.game_id, new_position[0], new_position[1],
                                                                         selected_enemy_square.unit_id)
                    self.game_controller.squares_dao.update_square_units(game.game_id, selected_enemy_square.x,
                                                                         selected_enemy_square.y,
                                                                         None)
                return True
        return False

    def _can_sabotage(self, selected_square, game):
        if selected_square.game_unit.has_used_power:
            return False

        squares = self.game_controller.squares_dao.get_all_squares(game.game_id)

        if selected_square.game_unit.unit_id == 6:
            unit = Commando(self.game_controller.cnx, game)
            if unit.has_adjacent_player(selected_square, squares):
                unit.use_special_power(selected_square, squares)
                self.game_controller.game_unit_dao.update_has_used_power(selected_square.game_unit.game_unit_id)
                print(
                    f"{selected_square.game_unit.game_unit_id} Rank: {selected_square.game_unit.rank} has used sabotage")
                return True

    def _attempt_use_enemy_power(self, selected_enemy_square, game):
        odds = Constants.ENEMY_ABILITY_ODDS
        squares = self.game_controller.squares_dao.get_all_squares(game.game_id)

        if selected_enemy_square.game_unit.has_used_power:
            return False

        if selected_enemy_square.game_unit.unit_id == 1:
            unit = Scout(self.game_controller.cnx, game)
        elif selected_enemy_square.game_unit.unit_id == 3:
            unit = Sniper(self.game_controller.cnx, game)
        elif selected_enemy_square.game_unit.unit_id == 4:
            unit = ShieldBearer(self.game_controller.cnx, game)
        elif selected_enemy_square.game_unit.unit_id == 5:
            unit = BattleMaster(self.game_controller.cnx, game)
        else:
            return False

        if random.random() > odds:
            return False

        if not selected_enemy_square.game_unit.has_used_power:
            unit.use_special_power(selected_enemy_square, squares)
            self.game_controller.game_unit_dao.update_has_used_power(selected_enemy_square.game_unit.game_unit_id)
            print(
                f"{selected_enemy_square.game_unit.game_unit_id} Rank: {selected_enemy_square.game_unit.rank} has used power")
            return True
        return False

    def _get_valid_positions(self, x, y, game_id):
        potential_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [pos for pos in potential_moves if
                self.game_controller.squares_dao.is_position_valid(game_id, pos[0], pos[1])]
