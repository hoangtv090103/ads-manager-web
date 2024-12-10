from configs.db import get_db_connection


class AdSizeFormat:
    def __init__(self, size_id=None, format_id=None):
        self.size_id = size_id
        self.format_id = format_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ad_size_format (
                size_id INTEGER NOT NULL,
                format_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (size_id, format_id),
                FOREIGN KEY (size_id) REFERENCES ads_zone_size(size_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ad_size_format (size_id, format_id)
            VALUES (%s, %s)
            ''', (self.size_id, self.format_id))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT asf.*, azs.ten_kich_thuoc, af.format_name
            FROM ad_size_format asf
            LEFT JOIN ads_zone_size azs ON asf.size_id = azs.size_id
            LEFT JOIN ads_format af ON asf.format_id = af.format_id
            WHERE asf.active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_format_id(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT asf.*, azs.ten_kich_thuoc
            FROM ad_size_format asf
            LEFT JOIN ads_zone_size azs ON asf.size_id = azs.size_id
            WHERE asf.format_id = %s AND asf.active = true
            ''', (format_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_size_id(size_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT asf.*, af.format_name
            FROM ad_size_format asf
            LEFT JOIN ads_format af ON asf.format_id = af.format_id
            WHERE asf.size_id = %s AND asf.active = true
            ''', (size_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ad_size_format 
            SET active = false 
            WHERE size_id = %s AND format_id = %s
            ''', (self.size_id, self.format_id))
            conn.commit()
