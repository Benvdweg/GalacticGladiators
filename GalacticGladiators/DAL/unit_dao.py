from GalacticGladiators.models.unit_model import UnitModel


class UnitDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def get_unit(self, unit_id):
        with self.cnx.cursor() as cursor:
            query = 'SELECT unit_id, type, special_power FROM units WHERE unit_id = %s'
            cursor.execute(query, (unit_id,))
            result = cursor.fetchone()
            if result:
                return UnitModel(*result)
            else:
                return None
