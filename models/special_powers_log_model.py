class SpecialPowersLogModel:
    def __init__(self, special_power_id, game_id, game_unit_id, power, turn_number, is_visible):
        self._special_power_id = special_power_id
        self._game_id = game_id
        self._game_unit_id = game_unit_id
        self._power = power
        self._turn_number = turn_number
        self._is_visible = is_visible

    @property
    def special_power_id(self):
        return self._special_power_id

    @property
    def game_id(self):
        return self._game_id

    @property
    def game_unit_id(self):
        return self._game_unit_id

    @property
    def power(self):
        return self._power

    @property
    def turn_number(self):
        return self._turn_number

    @property
    def is_visible(self):
        return self._is_visible
