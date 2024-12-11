from configs.db import get_db_connection


class PublisherStatus:
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3
    BLOCKED = 4

    def __init__(self, status_id=None, ten_trang_thai=""):
        self.status_id = status_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS publisher_status (
                status_id SERIAL PRIMARY KEY,
                ten_trang_thai VARCHAR(50) NOT NULL
            )
            ''')
            
            # Insert default statuses if they don't exist
            cursor.execute('SELECT COUNT(*) FROM publisher_status')
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                INSERT INTO publisher_status (status_id, ten_trang_thai) VALUES 
                (1, 'Hoạt động'),
                (2, 'Tạm khóa')
                ''')
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT status_id, ten_trang_thai FROM publisher_status')
            return cursor.fetchall()

    @staticmethod
    def get_by_name(ten_trang_thai):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT status_id FROM publisher_status WHERE ten_trang_thai = %s', (ten_trang_thai,))
            return cursor.fetchone()[0]
