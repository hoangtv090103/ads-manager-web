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