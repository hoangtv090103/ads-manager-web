from configs.db import get_db_connection

class PriceType:
    def __init__(self, pricetype_id=None, ten_loai_bang_gia=""):
        self.pricetype_id = pricetype_id
        self.ten_loai_bang_gia = ten_loai_bang_gia

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_type (
                pricetype_id SERIAL PRIMARY KEY,
                ten_loai_bang_gia VARCHAR(50),
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
            INSERT INTO price_type (ten_loai_bang_gia) 
            VALUES (?)
            ''', (self.ten_loai_bang_gia,))
            conn.commit()

    @staticmethod
    def get_all_types():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM price_type
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE price_type
            SET ten_loai_bang_gia = ?
            WHERE pricetype_id = ?
            ''', (self.ten_loai_bang_gia, self.pricetype_id))
            conn.commit()

    @staticmethod
    def delete_by_id(pricetype_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE price_type SET active = 0 WHERE pricetype_id = ?
            ''', (pricetype_id,))
            conn.commit()
