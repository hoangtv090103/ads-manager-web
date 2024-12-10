from configs.db import get_db_connection

class City:
    def __init__(self, city_id=None, ten_thanh_pho="", country_id=None,
                 mien="", created_at=None, updated_at=None, active=True):
        self.city_id = city_id
        self.ten_thanh_pho = ten_thanh_pho
        self.country_id = country_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.mien = mien
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS city (
                city_id SERIAL PRIMARY KEY,
                ten_thanh_pho VARCHAR(100) NOT NULL,
                country_id INTEGER NOT NULL,
                mien VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (country_id) REFERENCES country(country_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO city (city_id, ten_thanh_pho, country_id, mien)
            VALUES (%s, %s, %s, %s)
            ''', (self.city_id, self.ten_thanh_pho, self.country_id, self.mien))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT city_id, ten_thanh_pho, country_id, mien, created_at, updated_at, active FROM city WHERE active = true')
            rows = cursor.fetchall()
            if not rows:
                return []
            cities = [
                dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            return cities

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE city
            SET ten_thanh_pho = %s, country_id = %s, mien = %s
            WHERE city_id = %s
            ''', (self.ten_thanh_pho, self.country_id, self.mien, self.city_id))
            conn.commit()

    @staticmethod
    def delete_by_id(city_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE city SET active = 0 WHERE city_id = %s', (city_id,))
            conn.commit()
