from GalacticGladiators.models.square_log_model import SquareLogModel

class SquareLogDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def add_log(self, game, square):
        cursor = self.cnx.cursor()
        query = """
        INSERT INTO square_logs 
        (game_id, game_unit_id, square_type, turn_number, square_id) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (game.game_id, square.game_unit.game_unit_id, square.square_type, game.current_turn, square.id))
        self.cnx.commit()
        square_log_id = cursor.lastrowid
        cursor.close()
        return square_log_id

    def get_unit_log_count_on_square(self, game_id, game_unit_id, square_id):
        cursor = self.cnx.cursor()
        query = """
        SELECT COUNT(*) FROM square_logs
        WHERE game_id = %s AND game_unit_id = %s AND square_id = %s
        """
        cursor.execute(query, (game_id, game_unit_id, square_id))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0

    def get_logs_for_unit_on_square(self, game_id, game_unit_id, square_id):
        cursor = self.cnx.cursor()
        query = """
        SELECT * FROM square_logs
        WHERE game_id = %s AND game_unit_id = %s AND square_id = %s
        ORDER BY turn_number
        """
        cursor.execute(query, (game_id, game_unit_id, square_id))
        results = cursor.fetchall()
        cursor.close()
        return [SquareLogModel(*result) for result in results]

    def delete_logs_for_unit_on_square(self, game_id, game_unit_id, square_id):
        cursor = self.cnx.cursor()
        query = """
        DELETE FROM square_logs
        WHERE game_id = %s AND game_unit_id = %s AND square_id = %s
        """
        cursor.execute(query, (game_id, game_unit_id, square_id))
        self.cnx.commit()
        cursor.close()

    def delete_logs(self, logs):
        if not logs:
            return
        cursor = self.cnx.cursor()
        log_ids = [log.square_log_id for log in logs]
        placeholders = ', '.join(['%s'] * len(log_ids))
        query = f"""
        DELETE FROM square_logs
        WHERE square_log_id IN ({placeholders})
        """
        cursor.execute(query, log_ids)
        self.cnx.commit()
        cursor.close()
