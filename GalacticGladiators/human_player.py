from GalacticGladiators.player import Player
from GalacticGladiators.utils.constants import Constants
from GalacticGladiators.utils.game_states import GameState


class HumanPlayer(Player):
    def __init__(self, game_controller):
        super().__init__(game_controller)

    def handle_click(self, pos, game_id):
        self.game_controller.game = self.game_controller.game_dao.get_game(game_id)

        button_click_result = self.handle_button_click(pos)

        if not self.game_controller.game.has_ended:
            square_click_result = self.handle_square_click(pos)
        else:
            square_click_result = False

        if (button_click_result and not self.game_controller.game.has_ended) or square_click_result:
            self.game_controller.ai_player.move_random_enemy_unit(game_id, self.game_controller.game)
            self.game_controller.game_service.undo_powers(self.game_controller.game)
            self.game_controller.add_gold(self.game_controller.game)
            self.game_controller.game_dao.update_turn(self.game_controller.game.game_id)

    def handle_button_click(self, pos):
        for button in self.game_controller.buttons:
            if button.rect.collidepoint(pos):
                if button.name == "start_game":
                    self.game_controller.game_dao.start_game(self.game_controller.game.game_id)
                elif button.name == "main_menu":
                    self.game_controller.game_state['state'] = GameState.MENU
                elif button.name == "special_power":
                    game_unit = self.game_controller.squares_dao.get_square_by_id(
                        self.game_controller.game.selected_unit_square_id).game_unit.game_unit_id
                    unit_value = self.game_controller.units_map.get(game_unit)
                    unit_value.use_special_power(self.game_controller.squares_dao.get_square_by_id(self.game_controller.game.selected_unit_square_id),
                                                 self.game_controller.squares_dao.get_all_squares(self.game_controller.game.game_id))
                    self.game_controller.game_unit_dao.update_has_used_power(game_unit)
                    self.game_controller.game_dao.remove_game_unit_selected(self.game_controller.game.game_id)
                    return True
                return False

    def handle_square_click(self, pos):
        for rect, current_square in self.game_controller.squares:
            if rect.collidepoint(pos):
                key = (rect.x, rect.y)
                current_square = self.game_controller.squares_map[key]

                if current_square.y < 3 and not self.game_controller.game.has_started:
                    self.handle_pre_game_click(self.game_controller.game, current_square)
                    return False
                elif self.game_controller.game.has_started:
                    return self.handle_in_game_click(self.game_controller.game, current_square)
        return False

    def handle_pre_game_click(self, game, current_square):
        for unit_id, limit in Constants.UNIT_COUNTS.items():
            if self.game_controller.squares_dao.get_unit_amount_for_player(game.game_id, unit_id) < limit:
                player, enemy = self.game_controller.player_dao.get_players(game.game_id)
                game_unit_id = self.game_controller.game_unit_dao.create_game_unit(player.player_id, unit_id, game.game_id, True)

                previous_unit_id = current_square.unit_id

                self.game_controller.squares_dao.update_square_units(game.game_id, current_square.x, current_square.y, game_unit_id)

                if previous_unit_id:
                    self.game_controller.game_unit_dao.delete_game_unit(previous_unit_id)
                return

    def handle_in_game_click(self, game, current_square):
        previous_square = self.game_controller.squares_dao.get_square_by_id(game.selected_unit_square_id)
        if ((
                    previous_square and previous_square.id != current_square.id) or previous_square is None) and current_square.unit_id and current_square.game_unit.is_friendly:
            self.game_controller.game_dao.update_selected_unit(current_square.id, game.game_id)
            return False
        elif game.selected_unit_square_id:
            return self._handle_unit_movement(game, current_square, previous_square)

    def _handle_unit_movement(self, game, target_square, previous_square):
        if self._is_valid_move(target_square, previous_square):

            # Player decides to attack
            if target_square.unit_id and not target_square.game_unit.is_friendly:
                self.handle_attack(target_square, previous_square, game)

            # Player decides to move
            else:
                self._move_unit(game, target_square, previous_square)

            self.game_controller.game_dao.update_selected_unit(None, game.game_id)
            return True

        self.game_controller.game_dao.update_selected_unit(None, game.game_id)
        return False

    def _is_valid_move(self, current_square, previous_square):
        selected_x, selected_y = previous_square.x, previous_square.y
        return (((abs(current_square.x - selected_x) == 1 and current_square.y == selected_y) or
                 (abs(current_square.y - selected_y) == 1 and current_square.x == selected_x))
                and self.game_controller.game_service.get_unit_by_selected_square_id(previous_square.id).unit_id != 7)

    def _move_unit(self, game, current_square, previous_square):
        self.game_controller.game_service.squares_dao.update_square_units(game.game_id, current_square.x, current_square.y, previous_square.unit_id)
        self.game_controller.game_service.squares_dao.update_square_units(game.game_id, previous_square.x, previous_square.y, None)