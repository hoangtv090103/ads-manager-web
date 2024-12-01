from configs.db import get_db_connection


class TargetAudience:
    def __init__(self, ta_id=None, ten_nhom_doi_tuong="", ta_status_id=None,
                 trang_da_truy_cap="", hanh_vi_khach_hang=""):
        self.ta_id = ta_id
        self.ten_nhom_doi_tuong = ten_nhom_doi_tuong
        self.ta_status_id = ta_status_id
        self.trang_da_truy_cap = trang_da_truy_cap
        self.hanh_vi_khach_hang = hanh_vi_khach_hang

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_audience (
                ta_id SERIAL PRIMARY KEY,
                ten_nhom_doi_tuong VARCHAR(50),
                ta_status_id INTEGER,
                trang_da_truy_cap VARCHAR(50),
                hanh_vi_khach_hang VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ta_status_id) REFERENCES target_audience_status(ta_status_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO target_audience (ten_nhom_doi_tuong, ta_status_id, trang_da_truy_cap, hanh_vi_khach_hang)
            VALUES (%s, %s, %s, %s)
            ''', (self.ten_nhom_doi_tuong, self.ta_status_id, self.trang_da_truy_cap, self.hanh_vi_khach_hang))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT 
                    ta_id, 
                    ten_nhom_doi_tuong, 
                    ta_status_id, 
                    trang_da_truy_cap, 
                    hanh_vi_khach_hang, 
                    created_at, 
                    updated_at
                FROM target_audience 
                WHERE active = true''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(ta_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT 
                    ta_id, 
                    ten_nhom_doi_tuong, 
                    ta_status_id, 
                    trang_da_truy_cap, 
                    hanh_vi_khach_hang, 
                    created_at, 
                    updated_at
                FROM target_audience 
                WHERE ta_id = %s AND active = true''', (ta_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE target_audience
            SET ten_nhom_doi_tuong = %s, ta_status_id = %s, trang_da_truy_cap = %s, hanh_vi_khach_hang = %s
            WHERE ta_id = %s
            ''', (self.ten_nhom_doi_tuong, self.ta_status_id, self.trang_da_truy_cap, self.hanh_vi_khach_hang, self.ta_id))
            conn.commit()

    @staticmethod
    def delete_by_id(ta_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE target_audience SET active = false WHERE ta_id = %s
            ''', (ta_id,))
            conn.commit()
