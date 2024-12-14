from configs.db import get_db_connection

class AdsZoneSize:
    def __init__(self, size_id=None, ten_kich_thuoc=""):
        self.size_id = size_id
        self.ten_kich_thuoc = ten_kich_thuoc

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_zone_size (
                size_id SERIAL PRIMARY KEY,
                ten_kich_thuoc VARCHAR(50) NOT NULL,
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
            INSERT INTO ads_zone_size (ten_kich_thuoc) 
            VALUES (%s)
            ''', (self.ten_kich_thuoc,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM ads_zone_size
            WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_size_id(size_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM ads_zone_size
            LEFT JOIN ads_format ON ads_zone_size.format_id = ads_format.format_id
            LEFT JOIN campaign_type ON ads_format.campaign_type_id = campaign_type.campaign_type_id
            WHERE ads_zone_size.size_id = %s
            ''', (size_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_format_id(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM ads_zone_size 
            LEFT JOIN ads_format ON ads_zone_size.format_id = ads_format.format_id
            LEFT JOIN campaign_type ON ads_format.campaign_type_id = campaign_type.campaign_type_id
            WHERE ads_zone_size.format_id = %s
            ''', (format_id,))
            return cursor.fetchone()

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_size
            SET format_id = %s
            WHERE size_id = %s
            ''', (self.format_id, self.size_id))
            conn.commit()

    @staticmethod
    def delete_by_id(size_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_size SET active = 0 WHERE size_id = %s
            ''', (size_id,))
            conn.commit()
