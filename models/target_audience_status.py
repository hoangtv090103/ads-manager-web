from configs.db import get_db_connection


class TargetAudienceStatus:
    def __init__(self, ta_status_id=None, ten_trang_thai=""):
        self.ta_status_id = ta_status_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_audience_status (
                ta_status_id SERIAL PRIMARY KEY,
                ten_trang_thai VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')

            default_statuses = [
                ('Đã kết nối',),
                ('Chưa kết nối',)
            ]
            cursor.execute('''
            INSERT INTO target_audience_status (ten_trang_thai)
            VALUES (%s)
            ON CONFLICT (ta_status_id) DO NOTHING
            ''', default_statuses[0])

            cursor.execute('''
            INSERT INTO target_audience_status (ten_trang_thai)
            VALUES (%s)
            ON CONFLICT (ta_status_id) DO NOTHING
            ''', default_statuses[1])
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO target_audience_status (ten_trang_thai)
            VALUES (%s)
            ''', (self.ten_trang_thai,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT ta_status_id, ten_trang_thai, created_at, updated_at, active 
            FROM target_audience_status 
            WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE target_audience_status
            SET ten_trang_thai = ?
            WHERE ta_status_id = ?
            ''', (self.ten_trang_thai, self.ta_status_id))
            conn.commit()

    @staticmethod
    def delete_by_id(ta_status_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
        UPDATE target_audience_status SET active = 0 WHERE ta_status_id = ?
            ''', (ta_status_id,))
            conn.commit()
