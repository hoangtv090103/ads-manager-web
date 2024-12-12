from configs.db import get_db_connection


class TransactionSystem:
    def __init__(self, tran_id=None, customer_id=None, so_tien_nap=0.0, thoi_gian_nap=None, ghi_chu=""):
        self.tran_id = tran_id
        self.customer_id = customer_id
        self.so_tien_nap = so_tien_nap
        self.thoi_gian_nap = thoi_gian_nap
        self.ghi_chu = ghi_chu

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_system (
                tran_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                so_tien_nap DECIMAL(18,2),
                thoi_gian_nap TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                ghi_chu VARCHAR(200),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transaction_system (user_id, so_tien_nap, thoi_gian_nap, ghi_chu) 
            VALUES (%s, %s, %s, %s)
            ''', (self.user_id, self.so_tien_nap, self.thoi_gian_nap, self.ghi_chu))
        conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT u.ho_va_ten, ts.so_tien_nap, ts.thoi_gian_nap, ts.ghi_chu, ts.created_at 
            FROM transaction_system as ts 
            LEFT JOIN users as u ON ts.user_id = u.user_id
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE transaction_system
            SET user_id = ?, so_tien_nap = ?, thoi_gian_nap = ?, ghi_chu = ?
            WHERE tran_id = ?
            ''', (self.user_id, self.so_tien_nap, self.thoi_gian_nap, self.ghi_chu, self.tran_id))
            conn.commit()

    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE transaction_system SET active = false WHERE tran_id = %s
            ''', (self.tran_id,))
            conn.commit()
