from configs.db import get_db_connection

class GeoTarget:
    def __init__(self, geo_id=None, geogroup_id=None, ten_vi_tri_dia_ly=""):
        self.geo_id = geo_id
        self.geogroup_id = geogroup_id
        self.ten_vi_tri_dia_ly = ten_vi_tri_dia_ly

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS geo_target (
                geo_id SERIAL PRIMARY KEY,
                geogroup_id INTEGER,
                ten_vi_tri_dia_ly VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (geogroup_id) REFERENCES geo_group_target(geogroup_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO geo_target (geogroup_id, ten_vi_tri_dia_ly) 
            VALUES (?, ?)
            ''', (self.geogroup_id, self.ten_vi_tri_dia_ly))
            conn.commit()

    @staticmethod
    def get_all_geo_targets():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM geo_target')
            rows = cursor.fetchall()
            return rows

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE geo_target
            SET geogroup_id = ?, ten_vi_tri_dia_ly = ?
            WHERE geo_id = ?
            ''', (self.geogroup_id, self.ten_vi_tri_dia_ly, self.geo_id))
            conn.commit()

    @staticmethod
    def delete_by_id(geo_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE geo_target SET active = 0 WHERE geo_id = ?
            ''', (geo_id,))
            conn.commit()
