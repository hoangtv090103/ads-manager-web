from configs.db import get_db_connection


class ProductStatus:
    def __init__(self, productstatus_id=None, ten_trang_thai=""):
        self.productstatus_id = productstatus_id
        self.ten_trang_thai = ten_trang_thai

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_status (
                productstatus_id SERIAL PRIMARY KEY,
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
            INSERT INTO product_status (ten_trang_thai)
            VALUES (?)
            ''', (self.ten_trang_thai,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT productstatus_id, ten_trang_thai, created_at, updated_at, active FROM product_status WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
    @staticmethod
    def get_by_name(ten_trang_thai):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT productstatus_id FROM product_status WHERE ten_trang_thai = %s
            ''', (ten_trang_thai,))
            return cursor.fetchone()[0]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if self.productstatus_id:
                cursor.execute('''
                UPDATE product_status
                SET ten_trang_thai = %s, 
                updated_at = CURRENT_TIMESTAMP
                WHERE productstatus_id = %s
                ''', (self.ten_trang_thai, self.productstatus_id))
            else:
                cursor.execute('''
                INSERT INTO product_status (ten_trang_thai)
                VALUES (%s)
                ''', (self.ten_trang_thai,))
            conn.commit()

    @staticmethod
    def delete_by_id(productstatus_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE product_status SET active = 0 WHERE productstatus_id = %s
            ''', (productstatus_id,))
            conn.commit()
