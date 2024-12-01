from configs.db import get_db_connection


class DataSourceStatus:
    def __init__(self, status_id=None, status_name=""):
        self.status_id = status_id
        self.status_name = status_name

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_source_status (
                status_id SERIAL PRIMARY KEY,
                name VARCHAR(20) NOT NULL
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO data_source_status (status_id, name)
            VALUES (?, ?)
            ''', (self.status_id, self.name))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM data_source_status')
            return cursor.fetchall()
