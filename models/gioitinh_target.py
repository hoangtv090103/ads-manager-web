from configs.db import get_db_connection

class GioiTinhTarget:
    def __init__(self, gioitinh_id=None, ten_gioi_tinh=""):
        self.gioitinh_id = gioitinh_id
        self.ten_gioi_tinh = ten_gioi_tinh

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS gioi_tinh_target (
                gioitinh_id SERIAL PRIMARY KEY,
                ten_gioi_tinh VARCHAR(50),
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
            INSERT INTO gioi_tinh_target (ten_gioi_tinh) 
            VALUES (?)
            ''', (self.ten_gioi_tinh,))
            conn.commit()

    @staticmethod
    def get_all_gioitinh_targets():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM gioi_tinh_target
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE gioi_tinh_target
            SET ten_gioi_tinh = ?
            WHERE gioitinh_id = ?
            ''', (self.ten_gioi_tinh, self.gioitinh_id))
            conn.commit()

    @staticmethod
    def delete_by_id(gioitinh_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE GioiTinhTarget SET active = 0 WHERE gioitinh_id = ?
            ''', (gioitinh_id,))
            conn.commit()
