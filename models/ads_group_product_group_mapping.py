from configs.db import get_db_connection


class AdsGroupProductGroupMapping:
    def __init__(self, mapping_id=None, product_group_id=None):
        self.mapping_id = mapping_id
        self.product_group_id = product_group_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group_product_group_mapping (
                mapping_id SERIAL PRIMARY KEY,
                product_group_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (product_group_id) REFERENCES product_group(product_group_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group_product_group_mapping (product_group_id)
            VALUES (%s)
            RETURNING mapping_id
            ''', (self.product_group_id,))
            self.mapping_id = cursor.fetchone()[0]
            conn.commit()
            return self.mapping_id

    @staticmethod
    def get_by_product_group_id(product_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT mapping_id, product_group_id, created_at
            FROM ads_group_product_group_mapping 
            WHERE product_group_id = %s
            ''', (product_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_product_group_id(product_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT mapping_id, product_group_id, created_at
            FROM ads_group_product_group_mapping 
            WHERE product_group_id = %s
            ''', (product_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(mapping_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM ads_group_product_group_mapping 
            WHERE mapping_id = %s
            ''', (mapping_id,))
            conn.commit()
