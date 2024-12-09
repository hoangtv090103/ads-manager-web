from configs.db import get_db_connection


class DataSource:
    def __init__(self, data_source_id=None, ten_nguon="", filename="", file="",
                 user_id=None, active=1):
        self.data_source_id = data_source_id
        self.ten_nguon = ten_nguon
        self.filename = filename
        self.file = file
        self.user_id = user_id
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_source (
                data_source_id SERIAL PRIMARY KEY,
                ten_nguon VARCHAR(100) NOT NULL,
                filename VARCHAR(255) NOT NULL,
                file BYTEA NOT NULL,
                user_id INTEGER NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO data_source (ten_nguon, filename, file, user_id)
            VALUES (%s, %s, %s, %s)
            ''', (self.ten_nguon, self.filename, self.file, self.user_id))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ds.data_source_id, ds.ten_nguon, ds.file, u.username
                FROM data_source ds
                LEFT JOIN users u ON ds.user_id = u.user_id
                WHERE ds.active = true
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row))
                    for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE data_source 
            SET ten_nguon = %s, filename = %s, file = %s, user_id = %s, active = %s
                updated_at = CURRENT_TIMESTAMP
            WHERE data_source_id = %s
            ''', (self.ten_nguon, self.filename, self.file, self.user_id, self.active,
                  self.data_source_id))
            conn.commit()

    @staticmethod
    def delete(data_source_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE data_source SET active = 0 WHERE data_source_id = ?',
                (data_source_id,))
            conn.commit()
