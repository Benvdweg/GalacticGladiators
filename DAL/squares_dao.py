from models.square_model import SquareModel
from models.game_unit_model import GameUnitModel


class SquaresDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def create_square(self, game_id, x, y):
        cursor = self.cnx.cursor()
        query = ("INSERT INTO squares (game_id, position_x, position_y, square_type, unit_id) VALUES (%s, %s, %s, "
                 "NULL, NULL)")
        cursor.execute(query, (game_id, x, y))
        self.cnx.commit()
        square_id = cursor.lastrowid
        cursor.close()
        return square_id

    def place_special_field(self, game_id, x, y, type):
        cursor = self.cnx.cursor()
        query = "UPDATE squares SET square_type = %s WHERE game_id = %s AND position_x = %s AND position_y = %s"
        cursor.execute(query, (type, game_id, x, y))
        self.cnx.commit()
        cursor.close()

    def update_square_units(self, game_id, x, y, unit_id):
        cursor = self.cnx.cursor()
        query = "UPDATE squares SET unit_id = %s WHERE game_id = %s AND position_x = %s AND position_y = %s"
        cursor.execute(query, (unit_id, game_id, x, y))
        self.cnx.commit()
        cursor.close()

    def update_square_units_by_id(self, unit_id):
        cursor = self.cnx.cursor()
        query = "UPDATE squares SET unit_id = NULL WHERE unit_id = %s"
        cursor.execute(query, (unit_id,))
        self.cnx.commit()
        cursor.close()

    def get_unit_amount_for_player(self, game_id, unit_id):
        cursor = self.cnx.cursor()
        query = "SELECT COUNT(*) AS aantal_rijen FROM game_units WHERE game_id = %s AND unit_id = %s AND is_friendly"
        cursor.execute(query, (game_id, unit_id))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0

    def get_square(self, game_id, x, y):
        cursor = self.cnx.cursor()
        query = """
        SELECT s.square_id, s.game_id, s.position_x, s.position_y, s.square_type, s.unit_id,
               gu.*
        FROM squares s
        LEFT JOIN game_units gu ON s.unit_id = gu.game_unit_id
        WHERE s.game_id = %s AND s.position_x = %s AND s.position_y = %s
        """
        cursor.execute(query, (game_id, x, y))
        result = cursor.fetchone()
        cursor.close()

        if result:
            square_data = result[:6]
            game_unit_data = result[6:]
            game_unit = GameUnitModel(*game_unit_data) if game_unit_data[0] else None
            return SquareModel(*square_data, game_unit)
        else:
            return None

    def get_all_squares(self, game_id):
        cursor = self.cnx.cursor()
        query = """
        SELECT s.square_id, s.game_id, s.position_x, s.position_y, s.square_type, s.unit_id,
               gu.*
        FROM squares s
        LEFT JOIN game_units gu ON s.unit_id = gu.game_unit_id
        WHERE s.game_id = %s
        """
        cursor.execute(query, (game_id,))
        results = cursor.fetchall()
        cursor.close()

        squares = []
        for result in results:
            square_data = result[:6]
            game_unit_data = result[6:]
            game_unit = GameUnitModel(*game_unit_data) if game_unit_data[0] else None
            squares.append(SquareModel(*square_data, game_unit))

        return squares

    def place_enemy_unit(self, game_id, x, y, unit_id):
        query = "UPDATE squares SET unit_id = %s WHERE game_id = %s AND position_x = %s AND position_y = %s"
        cursor = self.cnx.cursor()
        cursor.execute(query, (unit_id, game_id, x, y))
        self.cnx.commit()
        cursor.close()

    def get_square_by_id(self, square_id):
        cursor = self.cnx.cursor()
        query = """
        SELECT s.square_id, s.game_id, s.position_x, s.position_y, s.square_type, s.unit_id,
               gu.*
        FROM squares s
        LEFT JOIN game_units gu ON s.unit_id = gu.game_unit_id
        WHERE s.square_id = %s
        """
        cursor.execute(query, (square_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            square_data = result[:6]
            game_unit_data = result[6:]
            game_unit = GameUnitModel(*game_unit_data) if game_unit_data[0] else None
            return SquareModel(*square_data, game_unit)
        else:
            return None

    def get_all_active_enemy_units(self, game_id):
        cursor = self.cnx.cursor()
        query = """
        SELECT s.square_id, s.game_id, s.position_x, s.position_y, s.square_type, s.unit_id,
               gu.*
        FROM squares s
        INNER JOIN game_units gu ON s.unit_id = gu.game_unit_id
        WHERE s.game_id = %s AND gu.is_friendly = FALSE AND gu.is_defeated = FALSE AND gu.unit_id != 7
        """
        cursor.execute(query, (game_id,))
        results = cursor.fetchall()
        cursor.close()

        enemy_units = [
            SquareModel(*result[:6], GameUnitModel(*result[6:]))
            for result in results
        ]

        return enemy_units

    def is_position_valid(self, game_id, x, y):
        cursor = self.cnx.cursor()
        query = """
        SELECT 1 
        FROM squares s
        LEFT JOIN game_units gu ON s.unit_id = gu.game_unit_id
        WHERE s.game_id = %s AND s.position_x = %s AND s.position_y = %s 
        AND (s.unit_id IS NULL OR (gu.is_friendly = TRUE AND gu.is_defeated = FALSE))
        LIMIT 1
        """
        cursor.execute(query, (game_id, x, y))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_game_unit_rank(self, square_id):
        query = "SELECT `gu`.`rank` FROM `squares` AS `s` JOIN `game_units` AS `gu` ON `s`.`unit_id` = `gu`.`game_unit_id` WHERE `s`.`square_id` = %s"

        with self.cnx.cursor() as cursor:
            cursor.execute(query, (square_id,))
            result = cursor.fetchone()

        return result[0] if result else None

    def get_all_gold_squares(self, game_id):
        query = """
                SELECT s.*, gu.* 
                FROM squares s
                LEFT JOIN game_units gu ON s.unit_id = gu.game_unit_id
                WHERE s.game_id = %s AND s.square_type = 'goldmine'
                """

        with self.cnx.cursor() as cursor:
            cursor.execute(query, (game_id,))
            results = cursor.fetchall()

        goldmine_squares = []
        for result in results:
            square_data = result[:6]
            game_unit_data = result[6:]
            game_unit = GameUnitModel(*game_unit_data) if game_unit_data[0] else None
            square = SquareModel(*square_data, game_unit)
            goldmine_squares.append(square)

        return goldmine_squares
