from configs.db import get_db_connection

class AdsGroupProductGroup:
    def __init__(self, id=None, ads_group_id=None, product_group_id=None):
        self.id = id
        self.ads_group_id = ads_group_id
        self.product_group_id = product_group_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group_product_group (
                id SERIAL PRIMARY KEY,
                ads_group_id INTEGER NOT NULL,
                product_group_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ads_group_id) REFERENCES ads_group(ads_group_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (product_group_id) REFERENCES product_group(group_id)
                    ON DELETE CASCADE,
                UNIQUE(ads_group_id, product_group_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group_product_group (ads_group_id, product_group_id)
            VALUES (%s, %s)
            RETURNING id
            ''', (self.ads_group_id, self.product_group_id))
            self.id = cursor.fetchone()[0]
            conn.commit()
            return self.id

    @staticmethod
    def get_by_ads_group_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT *
            FROM ads_group_product_group 
            LEFT JOIN product_group ON ads_group_product_group.product_group_id = product_group.product_group_id
            LEFT JOIN ads_group ON ads_group_product_group.ads_group_id = ads_group.ads_group_id
            WHERE ads_group_id = %s AND active = TRUE
            ''', (ads_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_product_group_id(product_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, ads_group_id, product_group_id 
            FROM ads_group_product_group 
            WHERE product_group_id = %s AND active = TRUE
            ''', (product_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(ads_group_id, product_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_group_product_group 
            SET active = FALSE 
            WHERE ads_group_id = %s AND product_group_id = %s
            ''', (ads_group_id, product_group_id))
            conn.commit()
