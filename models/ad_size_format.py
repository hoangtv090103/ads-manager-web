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

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ad_size_format (size_id, format_id)
            VALUES (%s, %s)
            RETURNING size_id, format_id
            ''', (self.size_id, self.format_id))
            size_id, format_id = cursor.fetchone()
            self.size_id = size_id
            self.format_id = format_id
            conn.commit()
            return self.size_id, self.format_id

    @staticmethod
    def get_by_size_id(size_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT size_id, format_id 
            FROM ad_size_format 
            WHERE size_id = %s AND active = TRUE
            ''', (size_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_format_id(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT size_id, format_id 
            FROM ad_size_format 
            WHERE format_id = %s AND active = TRUE
            ''', (format_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(size_id, format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ad_size_format 
            SET active = FALSE 
            WHERE size_id = %s AND format_id = %s
            ''', (size_id, format_id))
            conn.commit() 