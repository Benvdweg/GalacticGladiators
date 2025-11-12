class GameUnitModel:
    def __init__(self, game_unit_id, game_id, player_id, unit_id, has_used_power, rank, is_friendly, is_defeated, captured_at_turn):
        self._game_unit_id = game_unit_id
        self._game_id = game_id
        self._player_id = player_id
        self._unit_id = unit_id
        self._has_used_power = has_used_power
        self._rank = rank
        self._is_friendly = is_friendly
        self._is_defeated = is_defeated
        self._captured_at_turn = captured_at_turn

    @property
    def game_unit_id(self):
        return self._game_unit_id

    @property
    def game_id(self):
        return self._game_id

    @property
    def player_id(self):
        return self._player_id

    @property
    def unit_id(self):
        return self._unit_id

    @property
    def has_used_power(self):
        return self._has_used_power

    @property
    def rank(self):
        return self._rank

    @property
    def is_friendly(self):
        return self._is_friendly

    @property
    def is_defeated(self):
        return self._is_defeated

    @property
    def captured_at_turn(self):
        return self._captured_at_turn

    def __repr__(self):
        return (f"GameUnit(game_unit_id={self._game_unit_id}, game_id={self._game_id}, "
                f"player_id={self._player_id}, unit_id={self._unit_id}, "
                f"has_used_power={self._has_used_power}, rank={self._rank}"
                f"is_friendly={self._is_friendly}, is_defeated={self._is_defeated})")
