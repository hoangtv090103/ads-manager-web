from configs.db import get_db_connection


class CampStatus:
    def __init__(self, campstatus_id=None, ten_trang_thai=""):
        self.campstatus_id = campstatus_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_status (
                campstatus_id SERIAL PRIMARY KEY,
                ten_trang_thai VARCHAR(50) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM campaign_status')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(campstatus_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM campaign_status WHERE campstatus_id = %s', (campstatus_id,))
            return cursor.fetchone()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO campaign_status (ten_trang_thai) VALUES (%s)', (self.ten_trang_thai,))
            conn.commit()
            return cursor.lastrowid

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE campaign_status SET ten_trang_thai = %s WHERE campstatus_id = %s', (self.ten_trang_thai, self.campstatus_id))
            conn.commit()
            return cursor.lastrowid

    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE campaign_status SET active = FALSE WHERE campstatus_id = %s', (self.campstatus_id,))
            conn.commit()
            return cursor.lastrowid
