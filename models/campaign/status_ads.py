from configs.db import get_db_connection


class StatusAds:
    def __init__(self, status_id=None, ten_trang_thai=""):
        self.status_id = status_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_ads (
                status_id SERIAL PRIMARY KEY,
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
            INSERT INTO status_ads (ten_trang_thai)
            VALUES (?)
            ''', (self.ten_trang_thai,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT status_id, ten_trang_thai, created_at, updated_at, active 
                FROM status_ads 
                WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE status_ads
            SET ten_trang_thai = ?, updated_at = CURRENT_TIMESTAMP
            WHERE status_id = ?
            ''', (self.ten_trang_thai, self.status_id))
            conn.commit()

    @staticmethod
    def delete_by_id(status_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE status_ads SET active = 0 WHERE status_id = ?
            ''', (status_id,))
            conn.commit()
