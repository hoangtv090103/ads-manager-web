from configs.db import get_db_connection


class District:
    def __init__(self, district_id=None, ten_quan_huyen="", city_id=None,
                 created_at=None, updated_at=None, active=True):
        self.district_id = district_id
        self.ten_quan_huyen = ten_quan_huyen
        self.city_id = city_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS district (
                district_id SERIAL PRIMARY KEY,
                ten_quan_huyen VARCHAR(100) NOT NULL,
                city_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (city_id) REFERENCES city(city_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO district (district_id, ten_quan_huyen, city_id)
            VALUES (?, ?, ?)
            ''', (self.district_id, self.ten_quan_huyen, self.city_id))
            conn.commit()

    @staticmethod
    def get_all_districts():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT district_id, ten_quan_huyen, city_id, created_at, updated_at, active FROM district WHERE active = true')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE district
            SET ten_quan_huyen = ?, city_id = ?
            WHERE district_id = ?
            ''', (self.ten_quan_huyen, self.city_id, self.district_id))
            conn.commit()

    @staticmethod
    def delete_by_id(district_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE district SET active = 0 WHERE district_id = ?', (district_id,))
            conn.commit()
