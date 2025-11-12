from models.game_model import GameModel


class GameDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def get_all_games(self):
        with self.cnx.cursor() as cursor:
            cursor.execute(
                'SELECT game_id, has_started, has_ended, created_at, current_turn, selected_unit_square_id '
                'FROM games ORDER BY created_at DESC')
            results = cursor.fetchall()
            return [GameModel(*row) for row in results]

    def get_game(self, game_id):
        cursor = self.cnx.cursor()
        query = (
            "SELECT game_id, has_started, has_ended, created_at, current_turn, selected_unit_square_id "
            "FROM games WHERE game_id = %s")
        cursor.execute(query, (game_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return GameModel(*result)
        else:
            return None

    def create_game(self):
        cursor = self.cnx.cursor()
        query = "INSERT INTO games (has_started, has_ended, current_turn, created_at) VALUES (%s, %s, %s, NOW())"
        cursor.execute(query, (0, 0, 0))
        self.cnx.commit()
        game_id = cursor.lastrowid
        cursor.close()
        return game_id

    def start_game(self, game_id):
        cursor = self.cnx.cursor()
        query = "UPDATE games SET has_started = 1 WHERE game_id = %s"
        cursor.execute(query, (game_id,))
        self.cnx.commit()
        cursor.close()

    def update_selected_unit(self, square_id, game_id):
        cursor = self.cnx.cursor()
        query = "UPDATE games SET selected_unit_square_id = %s WHERE game_id = %s"
        cursor.execute(query, (square_id, game_id))
        self.cnx.commit()
        cursor.close()

    def update_turn(self, game_id):
        cursor = self.cnx.cursor()
        query = "UPDATE games SET current_turn = current_turn + 1 WHERE game_id = %s"
        cursor.execute(query, (game_id,))
        self.cnx.commit()
        cursor.close()

    def remove_game_unit_selected(self, game_id):
        cursor = self.cnx.cursor()
        query = "UPDATE games SET selected_unit_square_id = NULL WHERE game_id = %s"
        cursor.execute(query, (game_id,))
        self.cnx.commit()
        cursor.close()

    def end_game(self, game_id):
        cursor = self.cnx.cursor()
        query = "UPDATE games SET has_ended = 1 WHERE game_id = %s"
        cursor.execute(query, (game_id,))
        self.cnx.commit()
        cursor.close()
