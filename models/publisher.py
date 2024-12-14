from configs.db import get_db_connection

class Publisher:
    def __init__(self, publisher_id=None, ten_publisher="", email="", so_dien_thoai="", pub_status_id=None, created_at=None, updated_at=None, active=True, user_id=None):
        self.publisher_id = publisher_id
        self.ten_publisher = ten_publisher
        self.user_id = user_id
        self.email = email
        self.so_dien_thoai = so_dien_thoai
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS publisher (
                    publisher_id SERIAL PRIMARY KEY,
                    ten_publisher VARCHAR(100) NOT NULL,
                    user_id INTEGER NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    so_dien_thoai VARCHAR(20),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                        ON DELETE SET NULL
                )
                ''')
                conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO publisher (publisher_id, ten_publisher, email, so_dien_thoai, user_id)
            VALUES (%s, %s, %s, %s, %s)
            ''', (
                self.publisher_id, self.ten_publisher, self.email, self.so_dien_thoai, self.user_id))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT publisher_id, ten_publisher, email, so_dien_thoai, created_at, updated_at FROM publisher WHERE active = true')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
    @staticmethod
    def get_by_user_id(user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM publisher WHERE user_id = %s AND active = true',
                (user_id,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row)) if row else None

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE publisher
            SET ten_publisher = %s, email = %s, so_dien_thoai = %s, user_id = %s
            WHERE publisher_id = %s
            ''', (
                self.ten_publisher, self.email, self.so_dien_thoai, self.user_id, self.publisher_id))
            conn.commit()

    @staticmethod
    def delete(publisher_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE publisher SET active = false WHERE publisher_id = %s', (publisher_id,))
            conn.commit()

    @staticmethod
    def get_by_id(publisher_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM publisher 
                WHERE publisher_id = %s AND active = true
            ''', (publisher_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))
