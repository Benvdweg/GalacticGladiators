from functools import wraps


def power_expiration_check(turns_to_expire):
    def decorator(func):
        @wraps(func)
        def wrapper(self, game, power):
            if (game.current_turn - turns_to_expire) >= power.turn_number:
                self.special_powers_log_dao.delete_special_power_log(power.special_power_id)
                return func(self, game, power)
            return False

        return wrapper

    return decorator
