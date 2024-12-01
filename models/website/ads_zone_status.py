from configs.db import get_db_connection

class AdsZoneStatus:
    def __init__(self, zonestatus_id=None, ten_trang_thai=""):
        self.zonestatus_id = zonestatus_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_zone_status (
                zonestatus_id SERIAL PRIMARY KEY,
                ten_trang_thai VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_zone_status (ten_trang_thai) 
            VALUES (?)
            ''', (self.ten_trang_thai,))
            conn.commit()

    @staticmethod
    def get_all_statuses():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ads_zone_status')
            rows = cursor.fetchall()
            return rows

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_status
            SET ten_trang_thai = ?
            WHERE zonestatus_id = ?
            ''', (self.ten_trang_thai, self.zonestatus_id))
            conn.commit()

    @staticmethod
    def delete_by_id(zonestatus_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_status SET active = 0 WHERE zonestatus_id = ?
            ''', (zonestatus_id,))
            conn.commit()
