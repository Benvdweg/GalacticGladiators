class SquareModel:
    def __init__(self, square_id, game_id, x, y, square_type, unit_id, game_unit=None):
        self._id = square_id
        self._game_id = game_id
        self._x = x
        self._y = y
        self._square_type = square_type
        self._unit_id = unit_id
        self._game_unit = game_unit

    @property
    def id(self):
        return self._id

    @property
    def game_id(self):
        return self._game_id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def square_type(self):
        return self._square_type

    @property
    def unit_id(self):
        return self._unit_id

    @unit_id.setter
    def unit_id(self, value):
        self._unit_id = value

    @property
    def game_unit(self):
        return self._game_unit

    @game_unit.setter
    def game_unit(self, value):
        self._game_unit = value

    def __repr__(self):
        return (f"Square(square_id={self._id}, game_id={self._game_id}, x={self._x}, y={self._y}, "
                f"units_id={self._unit_id}, ")
