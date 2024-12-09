from configs.db import get_db_connection
class TransactionSystem:
    def __init__(self, tran_id=None, user_id=None, so_tien_nap=0,
                 thoi_gian_nap=None, ghi_chu="", created_at=None,
                 updated_at=None, active=True):
        self.tran_id = tran_id
        self.user_id = user_id
        self.so_tien_nap = so_tien_nap
        self.thoi_gian_nap = thoi_gian_nap
        self.ghi_chu = ghi_chu
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_system (
                tran_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                so_tien_nap DECIMAL(15,2),
                thoi_gian_nap TIMESTAMPTZ,
                ghi_chu TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit() 