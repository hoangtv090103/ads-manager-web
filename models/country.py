from configs.db import get_db_connection

class Country:
    def __init__(self, country_id=None, ten_quoc_gia="",
                 created_at=None, updated_at=None, status=True):
        self.country_id = country_id
        self.ten_quoc_gia = ten_quoc_gia
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS country (
                country_id SERIAL PRIMARY KEY,
                ten_quoc_gia VARCHAR(100) NOT NULL,
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
            INSERT INTO country (ten_quoc_gia)
            VALUES (?)
            ''', (self.ten_quoc_gia,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT country_id, ten_quoc_gia, created_at, updated_at, status FROM country WHERE status = true')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE Country
            SET ten_quoc_gia = ?, updated_at = CURRENT_TIMESTAMP
            WHERE country_id = ?
            ''', (self.ten_quoc_gia, self.country_id))
            conn.commit()

    @staticmethod
    def delete_by_id(country_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE Country SET status = 0 WHERE country_id = ?
            ''', (country_id,))
            conn.commit()
