from configs.db import get_db_connection
class SanPhamDichVuCam:
    def __init__(self, spcam_id=None, ten_san_pham=""):
        self.spcam_id = spcam_id
        self.ten_san_pham = ten_san_pham

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS san_pham_dich_vu_cam (
                spcam_id SERIAL PRIMARY KEY,
                ten_san_pham VARCHAR(50),
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
            INSERT INTO san_pham_dich_vu_cam (ten_san_pham) 
            VALUES (?)
            ''', (self.ten_san_pham,))
            conn.commit()

    @staticmethod
    def get_all_products():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM san_pham_dich_vu_cam
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE san_pham_dich_vu_cam
            SET ten_san_pham = ?
            WHERE spcam_id = ?
            ''', (self.ten_san_pham, self.spcam_id))
            conn.commit()

    @staticmethod
    def delete_by_id(spcam_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE san_pham_dich_vu_cam SET active = 0 WHERE spcam_id = ?
            ''', (spcam_id,))
            conn.commit()
