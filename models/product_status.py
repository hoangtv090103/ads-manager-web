from configs.db import get_db_connection
class ProductStatus:
    def __init__(self, product_status_id=None, ten_trang_thai="",
                 created_at=None, updated_at=None, active=True):
        self.product_status_id = product_status_id
        self.ten_trang_thai = ten_trang_thai
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_status (
                product_status_id SERIAL PRIMARY KEY,
                ten_trang_thai VARCHAR(50) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit() 