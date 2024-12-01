from configs.db import get_db_connection


class AdsFormat:
    def __init__(self, format_id=None, ads_type_id=None, ten_dinh_dang=""):
        self.format_id = format_id
        self.ads_type_id = ads_type_id
        self.ten_dinh_dang = ten_dinh_dang

    def __str__(self):
        return f"AdsFormat(Type ID: {self.ads_type_id}, Format ID: {self.format_id}, Name: {self.ten_dinh_dang})"

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_format (
                format_id SERIAL PRIMARY KEY,
                ads_type_id INTEGER NOT NULL,
                ten_dinh_dang VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ads_type_id) REFERENCES ads_type(ads_type_id)
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_format (ads_type_id, ten_dinh_dang) 
            VALUES (?, ?)
            ''', (self.ads_type_id, self.ten_dinh_dang))
            conn.commit()

    @staticmethod
    def get_all_ads_formats():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ads_type_id, format_id, ten_dinh_dang, created_at, updated_at, active 
                FROM ads_format
                WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ads_format
                SET ads_type_id = ?, ten_dinh_dang = ?
                WHERE format_id = ?
                ''', (self.ads_type_id, self.ten_dinh_dang, self.format_id))
            conn.commit()

    @staticmethod
    def delete_by_id(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE ads_format SET active = false WHERE format_id = %s', (format_id,))
            conn.commit()
