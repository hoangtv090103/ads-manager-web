from configs.db import get_db_connection


class WebsiteStatus:
    def __init__(self, webstatus_id=None, ten_trang_thai=""):
        self.webstatus_id = webstatus_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS website_status (
                webstatus_id SERIAL PRIMARY KEY,
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
            INSERT INTO website_status (ten_trang_thai) 
            VALUES (?)
            ''', (self.ten_trang_thai,))
            conn.commit()

    @staticmethod
    def get_all_statuses():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT webstatus_id, ten_trang_thai, created_at, updated_at, active 
            FROM website_status WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE website_status
            SET ten_trang_thai = ?
            WHERE webstatus_id = ?
            ''', (self.ten_trang_thai, self.webstatus_id))
            conn.commit()

    @staticmethod
    def delete_by_id(webstatus_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE website_status SET active = 0 WHERE webstatus_id = ?
            ''', (webstatus_id,))
            conn.commit()
