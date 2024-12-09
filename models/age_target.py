from configs.db import get_db_connection

class AgeTarget:
    def __init__(self, age_id=None, ten_do_tuoi=""):
        self.age_id = age_id
        self.ten_do_tuoi = ten_do_tuoi

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS age_target (
                age_id SERIAL PRIMARY KEY,
                ten_do_tuoi VARCHAR(50),
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
            INSERT INTO age_target (ten_do_tuoi) 
            VALUES (?)
            ''', (self.ten_do_tuoi,))
            conn.commit()

    @staticmethod
    def get_all_age_targets():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM age_target')
            rows = cursor.fetchall()
            return rows

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE age_target
            SET ten_do_tuoi = ?
            WHERE age_id = ?
            ''', (self.ten_do_tuoi, self.age_id))
            conn.commit()

    @staticmethod
    def delete_by_id(age_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE age_target SET active = 0 WHERE age_id = ?
            ''', (age_id,))
            conn.commit()
