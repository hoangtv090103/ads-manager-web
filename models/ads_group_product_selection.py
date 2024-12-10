from configs.db import get_db_connection


class AdsGroupProductSelection:
    def __init__(self, selection_id=None, ads_group_id=None, selection_type=None):
        self.selection_id = selection_id
        self.ads_group_id = ads_group_id
        self.selection_type = selection_type

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group_product_selection (
                selection_id SERIAL PRIMARY KEY,
                ads_group_id INTEGER NOT NULL,
                selection_type VARCHAR(50) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ads_group_id) REFERENCES ads_group(ads_group_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group_product_selection (ads_group_id, selection_type)
            VALUES (%s, %s)
            RETURNING selection_id
            ''', (self.ads_group_id, self.selection_type))
            self.selection_id = cursor.fetchone()[0]
            conn.commit()
            return self.selection_id

    @staticmethod
    def get_by_ads_group_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT selection_id, ads_group_id, selection_type, created_at
            FROM ads_group_product_selection 
            WHERE ads_group_id = %s AND active = TRUE
            ''', (ads_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_selection_type(selection_type):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT selection_id, ads_group_id, selection_type, created_at
            FROM ads_group_product_selection 
            WHERE selection_type = %s AND active = TRUE
            ''', (selection_type,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(selection_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_group_product_selection 
            SET active = FALSE 
            WHERE selection_id = %s
            ''', (selection_id,))
            conn.commit()
