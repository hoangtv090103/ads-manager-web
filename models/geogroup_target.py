from configs.db import get_db_connection

class GeoGroupTarget:
    def __init__(self, geogroup_id=None, ten_nhom_dia_ly=""):
        self.geogroup_id = geogroup_id
        self.ten_nhom_dia_ly = ten_nhom_dia_ly

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS geo_group_target (
                geogroup_id SERIAL PRIMARY KEY,
                ten_nhom_dia_ly VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO geo_group_target (ten_nhom_dia_ly) 
            VALUES (?)
            ''', (self.ten_nhom_dia_ly,))
            conn.commit()

    @staticmethod
    def get_all_geogroup_targets():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM geo_group_target
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE geo_group_target
            SET ten_nhom_dia_ly = ?
            WHERE geogroup_id = ?
            ''', (self.ten_nhom_dia_ly, self.geogroup_id))
            conn.commit()

    @staticmethod
    def delete_by_id(geogroup_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE geo_group_target SET active = 0 WHERE geogroup_id = ?
            ''', (geogroup_id,))
            conn.commit()
