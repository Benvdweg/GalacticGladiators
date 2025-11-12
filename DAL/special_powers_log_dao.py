from models.special_powers_log_model import SpecialPowersLogModel


class SpecialPowersLogDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def add_special_power_log(self, game_id, game_unit_id, power, turn_number, is_visible):
        cursor = self.cnx.cursor()
        query = ("INSERT INTO special_powers_log (game_id, game_unit_id, power, turn_number, is_visible) VALUES (%s, "
                 "%s, %s, %s, %s)")
        cursor.execute(query, (game_id, game_unit_id, power, turn_number, is_visible))
        self.cnx.commit()
        cursor.close()

    def get_all_special_powers_log(self, game_id):
        with self.cnx.cursor() as cursor:
            query = ('SELECT special_power_id, game_id, game_unit_id, power, turn_number, is_visible '
                     'FROM special_powers_log WHERE game_id = %s')
            cursor.execute(query, (game_id,))
            results = cursor.fetchall()
            return [SpecialPowersLogModel(*row) for row in results]

    def get_special_power_logs_for_game_unit(self, game_unit_id, power_id, is_visible):
        with self.cnx.cursor() as cursor:
            query = ('SELECT special_power_id, game_id, game_unit_id, power, turn_number, is_visible '
                     'FROM special_powers_log WHERE game_unit_id = %s AND power = %s AND is_visible = %s')
            cursor.execute(query, (game_unit_id, power_id, is_visible))
            results = cursor.fetchall()
            return [SpecialPowersLogModel(*row) for row in results]

    def delete_special_power_log(self, special_power_id):
        cursor = self.cnx.cursor()

        query = "DELETE FROM special_powers_log WHERE special_power_id = %s"
        cursor.execute(query, (special_power_id,))

        self.cnx.commit()
        cursor.close()
