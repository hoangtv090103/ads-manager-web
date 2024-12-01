from configs.db import get_db_connection


class Publisher:
    def __init__(self, publisher_id=None, ten_publisher="", email="", so_dien_thoai="", password="", pub_status_id=None):
        self.publisher_id = publisher_id
        self.ten_publisher = ten_publisher
        self.email = email
        self.so_dien_thoai = so_dien_thoai
        self.password = password
        self.pub_status_id = pub_status_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS publisher (
                publisher_id SERIAL PRIMARY KEY,
                ten_publisher VARCHAR(50),
                email VARCHAR(50),
                so_dien_thoai VARCHAR(12),
                password VARCHAR(100),
                pub_status_id INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (pub_status_id) REFERENCES publisher_status(status_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO publisher (publisher_id, ten_publisher, email, so_dien_thoai, password, pub_status_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
            self.publisher_id, self.ten_publisher, self.email, self.so_dien_thoai, self.password, self.pub_status_id))
            conn.commit()

    @staticmethod
    def get_all_publishers():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT publisher_id, ten_publisher, email, so_dien_thoai, password, pub_status_id, created_at, updated_at, status FROM publisher WHERE active = true')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE publisher
            SET ten_publisher = ?, email = ?, so_dien_thoai = ?, password = ?, pub_status_id = ?
            WHERE publisher_id = ?
            ''', (
            self.ten_publisher, self.email, self.so_dien_thoai, self.password, self.pub_status_id, self.publisher_id))
            conn.commit()

    @staticmethod
    def delete_by_id(publisher_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE publisher SET active = 0 WHERE publisher_id = ?', (publisher_id,))
            conn.commit()
