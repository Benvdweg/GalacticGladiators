import random
from abc import ABC, abstractmethod

from GalacticGladiators.DAL.game_dao import GameDAO
from GalacticGladiators.DAL.game_unit_dao import GameUnitDAO
from GalacticGladiators.DAL.player_dao import PlayerDAO
from GalacticGladiators.DAL.special_powers_log_dao import SpecialPowersLogDAO
from GalacticGladiators.DAL.squares_dao import SquaresDAO


class Unit(ABC):
    def __init__(self, cnx, game):
        self.game_dao = GameDAO(cnx)
        self.squares_dao = SquaresDAO(cnx)
        self.game_unit_dao = GameUnitDAO(cnx)
        self.player_dao = PlayerDAO(cnx)
        self.special_powers_log_dao = SpecialPowersLogDAO(cnx)
        self.game = game
        self.is_bot = None

    @abstractmethod
    def use_special_power(self, current_square, squares):
        pass

    def enemy_activated_shield_bearer(self, current_square):
        self.is_bot = not current_square.game_unit.is_friendly
        shield_bearers = self.game_unit_dao.get_game_units_of_type(4, current_square.game_id, self.is_bot)

        for game_unit in shield_bearers:
            if self.special_powers_log_dao.get_special_power_logs_for_game_unit(game_unit.game_unit_id, 4, False):
                enemy_shield_bearers = self.game_unit_dao.get_game_units_of_type(4, current_square.game_id,
                                                                                 not self.is_bot)
                for enemy in enemy_shield_bearers:
                    self.special_powers_log_dao.add_special_power_log(current_square.game_id, enemy.game_unit_id, 4,
                                                                      self.game_dao.get_game(
                                                                          current_square.game_id).current_turn, True)
                return True
        return False


class Scout(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        if self.enemy_activated_shield_bearer(current_square):
            return

        self.special_powers_log_dao.add_special_power_log(current_square.game_id, current_square.unit_id, "1",
                                                          self.game_dao.get_game(current_square.game_id).current_turn,
                                                          False)


class Infantry(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        pass


class Sniper(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        if self.enemy_activated_shield_bearer(current_square):
            return

        for square in squares:
            if square.game_unit:
                distance = abs(current_square.x - square.x) + abs(current_square.y - square.y)
                if self.is_bot:
                    # Bot logic: Attack friendly units
                    if distance <= 4 and square.game_unit.is_friendly and square.square_type != "coverage":
                        dice_result = random.randint(1, 6)
                        if dice_result >= 5:
                            self.game_unit_dao.defeat_unit(square.game_unit.game_unit_id, self.game)
                            self.squares_dao.update_square_units_by_id(square.game_unit.game_unit_id)
                        self.game_unit_dao.defeat_unit(current_square.game_unit.game_unit_id, self.game)
                        self.squares_dao.update_square_units_by_id(current_square.game_unit.game_unit_id)
                        return
                else:
                    # Non-bot logic: Attack non-friendly units
                    if distance <= 4 and not square.game_unit.is_friendly and square.square_type != "coverage":
                        dice_result = random.randint(1, 6)
                        if dice_result >= 5:
                            self.game_unit_dao.defeat_unit(square.game_unit.game_unit_id, self.game)
                            self.squares_dao.update_square_units_by_id(square.game_unit.game_unit_id)
                        self.game_unit_dao.defeat_unit(current_square.game_unit.game_unit_id, self.game)
                        self.squares_dao.update_square_units_by_id(current_square.game_unit.game_unit_id)
                        return
        self.game_unit_dao.defeat_unit(current_square.game_unit.game_unit_id, self.game)
        self.squares_dao.update_square_units_by_id(current_square.game_unit.game_unit_id)


class ShieldBearer(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        if self.enemy_activated_shield_bearer(current_square):
            return

        self.special_powers_log_dao.add_special_power_log(current_square.game_id, current_square.unit_id, "4",
                                                          self.game_dao.get_game(current_square.game_id).current_turn,
                                                          False)


class BattleMaster(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        if self.enemy_activated_shield_bearer(current_square):
            return

        squares = self.squares_dao.get_all_squares(current_square.game_id)

        for square in squares:
            if square.game_unit:
                distance = abs(current_square.x - square.x) + abs(current_square.y - square.y)
                if distance == 1:
                    if self.is_bot:
                        # Bot logic: Update the ranks of non friendly units
                        if not square.game_unit.is_friendly:
                            self.game_unit_dao.update_rank(square.unit_id, 1)
                            self.special_powers_log_dao.add_special_power_log(
                                current_square.game_id,
                                square.unit_id,
                                "5",
                                self.game_dao.get_game(current_square.game_id).current_turn, False
                            )
                    else:
                        # Non-bot logic: Update the ranks of friendly units
                        if square.game_unit.is_friendly:
                            self.game_unit_dao.update_rank(square.unit_id, 1)
                            self.special_powers_log_dao.add_special_power_log(
                                current_square.game_id,
                                square.unit_id,
                                "5",
                                self.game_dao.get_game(current_square.game_id).current_turn, False
                            )


class Commando(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        if self.enemy_activated_shield_bearer(current_square):
            return

        for square in squares:
            if square.game_unit:
                distance = abs(current_square.x - square.x) + abs(current_square.y - square.y)
                if distance == 1 and square.square_type != "coverage":
                    if self.is_bot:
                        # Bot logic: change friendly units to not friendly
                        if square.game_unit.is_friendly:
                            self.game_unit_dao.update_unit_is_friendly(False, square.unit_id)
                            return
                    else:
                        # Non-bot logic: change not friendly units to friendly
                        if not square.game_unit.is_friendly:
                            self.game_unit_dao.update_unit_is_friendly(True, square.unit_id)
                            return

    def has_adjacent_player(self, current_square, squares):
        for square in squares:
            if square.game_unit and square.game_unit.is_friendly:
                distance = abs(current_square.x - square.x) + abs(current_square.y - square.y)
                if distance == 1:
                    return True

        return False


class Flag(Unit):
    def __init__(self, cnx, game):
        super().__init__(cnx, game)

    def use_special_power(self, current_square, squares):
        pass
