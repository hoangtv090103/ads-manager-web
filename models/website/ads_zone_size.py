from configs.db import get_db_connection

class AdsZoneSize:
    def __init__(self, size_id=None, ten_kich_thuoc="", kich_thuoc=""):
        self.size_id = size_id
        self.ten_kich_thuoc = ten_kich_thuoc
        self.kich_thuoc = kich_thuoc

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_zone_size (
                size_id SERIAL PRIMARY KEY,
                ten_kich_thuoc VARCHAR(50),
                kich_thuoc VARCHAR(50),
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
            INSERT INTO ads_zone_size (ten_kich_thuoc, kich_thuoc) 
            VALUES (?, ?)
            ''', (self.ten_kich_thuoc, self.kich_thuoc))
            conn.commit()

    @staticmethod
    def get_all_sizes():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM ads_zone_size
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_size
            SET ten_kich_thuoc = ?, kich_thuoc = ?
            WHERE size_id = ?
            ''', (self.ten_kich_thuoc, self.kich_thuoc, self.size_id))
            conn.commit()

    @staticmethod
    def delete_by_id(size_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_size SET active = 0 WHERE size_id = ?
            ''', (size_id,))
            conn.commit()
