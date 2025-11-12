from abc import ABC

from utils.constants import Constants


class Player(ABC):
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def handle_attack(self, enemy_square, player_square, game):
        enemy_bonus = 1 if enemy_square.square_type == "elevated" else 0
        player_bonus = 1 if player_square.square_type == "elevated" else 0

        enemy_strength = enemy_square.game_unit.rank + enemy_bonus
        player_strength = player_square.game_unit.rank + player_bonus

        if self.game_controller.has_special_power_logs(player_square.unit_id, 1, False):
            print(f"Player has won: {player_strength} VS {enemy_strength}")
            self.game_controller.game_unit_dao.defeat_unit(enemy_square.game_unit.game_unit_id, game)
            self.game_controller.squares_dao.update_square_units(game.game_id, enemy_square.x, enemy_square.y, None)

        elif enemy_strength > player_strength or self.game_controller.has_special_power_logs(enemy_square.unit_id, 1, False):
            print(f"Enemy has won: {enemy_strength} VS {player_strength}")
            self.game_controller.game_unit_dao.defeat_unit(player_square.game_unit.game_unit_id, game)
            self.game_controller.squares_dao.update_square_units(game.game_id, player_square.x, player_square.y, None)

            if player_square.game_unit.unit_id == Constants.FLAG_ID:
                self.game_controller.calculate_score(game, True)
        elif enemy_strength < player_strength:
            print(f"Player has won: {player_strength} VS {enemy_strength}")
            self.game_controller.game_unit_dao.defeat_unit(enemy_square.game_unit.game_unit_id, game)
            self.game_controller.squares_dao.update_square_units(game.game_id, enemy_square.x, enemy_square.y, None)

            if enemy_square.game_unit.unit_id == Constants.FLAG_ID:
                self.game_controller.game_service.calculate_score(game, False)
        else:
            print(f"It's a draw: {player_strength} VS {enemy_strength}")
            self.game_controller.game_unit_dao.defeat_unit(enemy_square.game_unit.game_unit_id, game)
            self.game_controller.squares_dao.update_square_units(game.game_id, enemy_square.x, enemy_square.y, None)
            self.game_controller.game_unit_dao.defeat_unit(player_square.game_unit.game_unit_id, game)
            self.game_controller.squares_dao.update_square_units(game.game_id, player_square.x, player_square.y, None)