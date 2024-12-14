from configs.db import get_db_connection


class PriceType:
    def __init__(self, price_type_id=None, price_type_name=""):
        self.price_type_id = price_type_id
        self.price_type_name = price_type_name

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_type (
                price_type_id SERIAL PRIMARY KEY,
                price_type_name VARCHAR(50) NOT NULL,
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
            INSERT INTO price_type (price_type_name) 
            VALUES (%s)
            ''', (self.price_type_name,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM price_type
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
    @staticmethod
    def get_by_name(price_type_name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM price_type WHERE price_type_name = %s
            ''', (price_type_name,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row)) if row else None    
        
    @staticmethod
    def get_by_id(price_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM price_type WHERE price_type_id = %s', (price_type_id,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row)) if row else None

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE price_type
            SET price_type_name = %s
            WHERE price_type_id = %s
            ''', (self.price_type_name, self.price_type_id))
            conn.commit()

    @staticmethod
    def delete_by_id(price_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE price_type SET active = 0 WHERE price_type_id = %s
            ''', (price_type_id,))
            conn.commit()
