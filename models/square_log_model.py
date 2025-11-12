class SquareLogModel:
    def __init__(self, square_log_id, game_id, game_unit_id, square_type, turn_number, square_id):
        self.square_log_id = square_log_id
        self.game_id = game_id
        self.game_unit_id = game_unit_id
        self.square_id = square_id
        self.square_type = square_type
        self.turn_number = turn_number

    def __repr__(self):
        return (f"SquareLogModel(square_log_id={self.square_log_id}, "
                f"game_id={self.game_id}, "
                f"game_unit_id={self.game_unit_id}, "
                f"square_id={self.square_id}, "
                f"turn_number={self.turn_number})")

    def __eq__(self, other):
        if not isinstance(other, SquareLogModel):
            return False
        return (self.square_log_id == other.square_log_id and
                self.game_id == other.game_id and
                self.game_unit_id == other.game_unit_id and
                self.square_id == other.square_id and
                self.square_type == other.square_type,
                self.turn_number == other.turn_number)

    def __hash__(self):
        return hash((self.square_log_id, self.game_id, self.game_unit_id, self.square_id, self.turn_number))
