class UnitModel:
    def __init__(self, unit_id, type, special_power):
        self._unit_id = unit_id
        self._type = type
        self._special_power = special_power

    @property
    def unit_id(self):
        return self._unit_id

    @property
    def type(self):
        return self._type

    @property
    def special_power(self):
        return self._special_power