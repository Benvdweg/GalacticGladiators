from models.game_unit_model import GameUnitModel


class GameUnitDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def create_game_unit(self, player_id, unit_id, game_id, is_friendly):
        cursor = self.cnx.cursor()

        rank = 0 if unit_id == 7 else unit_id

        query = ("INSERT INTO game_units (game_id, player_id, unit_id, has_used_power, `rank`, is_friendly, is_defeated) VALUES (%s, "
                 "%s, %s, FALSE, %s, %s, FALSE)")
        cursor.execute(query, (game_id, player_id, unit_id, rank, is_friendly))
        self.cnx.commit()
        game_unit_id = cursor.lastrowid
        cursor.close()
        return game_unit_id

    def update_unit_is_friendly(self, is_friendly, game_unit_id):
        cursor = self.cnx.cursor()
        query = "UPDATE game_units SET is_friendly = %s WHERE game_unit_id = %s"
        cursor.execute(query, (is_friendly, game_unit_id,))
        self.cnx.commit()
        cursor.close()

    def update_rank(self, game_unit_id, amount):
        cursor = self.cnx.cursor()
        query = "UPDATE game_units SET `rank` = `rank` + %s WHERE game_unit_id = %s"
        cursor.execute(query, (amount, game_unit_id,))
        self.cnx.commit()
        cursor.close()

    def update_has_used_power(self, game_unit_id):
        cursor = self.cnx.cursor()
        query = "UPDATE game_units SET has_used_power = 1 WHERE game_unit_id = %s"
        cursor.execute(query, (game_unit_id,))
        self.cnx.commit()
        cursor.close()

    def defeat_unit(self, game_unit_id, game):
        cursor = self.cnx.cursor()
        query = "UPDATE game_units SET is_defeated = TRUE, captured_at_turn = %s WHERE game_unit_id = %s"
        cursor.execute(query, (game.current_turn, game_unit_id,))
        self.cnx.commit()
        cursor.close()

    def get_game_unit(self, square_id):
        query = "SELECT u.* FROM game_units u JOIN squares s ON s.unit_id = u.game_unit_id WHERE s.square_id = %s"

        with self.cnx.cursor() as cursor:
            cursor.execute(query, (square_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return GameUnitModel(*result)
            else:
                return None

    def get_all_game_units(self, game_id):
        query = "SELECT u.* FROM game_units u JOIN squares s ON s.unit_id = u.game_unit_id WHERE s.game_id = %s"

        with self.cnx.cursor() as cursor:
            cursor.execute(query, (game_id,))
            results = cursor.fetchall()
            cursor.close()
            return [GameUnitModel(*row) for row in results]

    def get_captured_enemies(self, game_id):
        cursor = self.cnx.cursor()
        query = "SELECT * FROM game_units WHERE game_id = %s AND is_defeated is True AND is_friendly is False"
        cursor.execute(query, (game_id,))
        results = cursor.fetchall()
        cursor.close()
        return [GameUnitModel(*row) for row in results]

    def get_captured_from_player(self, game_id):
        cursor = self.cnx.cursor()
        query = "SELECT * FROM game_units WHERE game_id = %s AND is_defeated is True AND is_friendly is True"
        cursor.execute(query, (game_id,))
        results = cursor.fetchall()
        cursor.close()
        return [GameUnitModel(*row) for row in results]

    def delete_game_unit(self, game_unit_id):
        cursor = self.cnx.cursor()

        update_squares_query = "UPDATE squares SET unit_id = NULL WHERE unit_id = %s"
        cursor.execute(update_squares_query, (game_unit_id,))

        delete_game_unit_query = "DELETE FROM game_units WHERE game_unit_id = %s"
        cursor.execute(delete_game_unit_query, (game_unit_id,))

        self.cnx.commit()
        cursor.close()

    def get_game_units_of_type(self, unit_id, game_id, is_friendly):
        with self.cnx.cursor() as cursor:
            query = ('SELECT *'
                     'FROM game_units WHERE unit_id = %s AND game_id = %s AND is_friendly = %s')
            cursor.execute(query, (unit_id, game_id, is_friendly,))
            results = cursor.fetchall()
            return [GameUnitModel(*row) for row in results]
