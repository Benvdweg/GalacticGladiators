class GameModel:
    def __init__(self, game_id, has_started, has_ended, created_at, current_turn, selected_unit_square_id):
        self._game_id = game_id
        self._has_started = has_started
        self._has_ended = has_ended
        self._created_at = created_at
        self._current_turn = current_turn
        self._selected_unit_square_id = selected_unit_square_id

    @property
    def game_id(self):
        return self._game_id

    @property
    def has_started(self):
        return self._has_started

    @property
    def has_ended(self):
        return self._has_ended

    @property
    def created_at(self):
        return self._created_at

    @property
    def current_turn(self):
        return self._current_turn

    @property
    def selected_unit_square_id(self):
        return self._selected_unit_square_id

