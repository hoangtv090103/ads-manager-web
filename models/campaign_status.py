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
                ten_trang_thai VARCHAR(50) NOT NULL UNIQUE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            cursor.execute('''
            INSERT INTO campaign_status (ten_trang_thai) VALUES ('Đang chạy'), ('Chưa chạy'), ('Tạm dừng'), ('Lỗi'), ('Hoàn thành'), ('Chưa hoàn thành')
            ON CONFLICT (ten_trang_thai) DO NOTHING
            ''')
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT campstatus_id, ten_trang_thai, created_at, updated_at, active
            FROM campaign_status
            WHERE active = TRUE
            ''')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(campstatus_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM campaign_status WHERE campstatus_id = %s', (campstatus_id,))
            return cursor.fetchone()
        
    @staticmethod
    def get_by_name(ten_trang_thai):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT campstatus_id FROM campaign_status WHERE ten_trang_thai ILIKE %s', (ten_trang_thai,))
            return cursor.fetchone()[0]

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO campaign_status (ten_trang_thai) VALUES (%s)', (self.ten_trang_thai,))
            conn.commit()
            return cursor.lastrowid

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE campaign_status SET ten_trang_thai = %s WHERE campstatus_id = %s',
                           (self.ten_trang_thai, self.campstatus_id))
            conn.commit()
            return cursor.lastrowid

    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE campaign_status SET active = FALSE WHERE campstatus_id = %s', (self.campstatus_id,))
            conn.commit()
            return cursor.lastrowid
