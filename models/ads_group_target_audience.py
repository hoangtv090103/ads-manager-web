from configs.db import get_db_connection

class AdsGroupTargetAudience:
    def __init__(self, id=None, ads_group_id=None, ta_id=None):
        self.id = id
        self.ads_group_id = ads_group_id
        self.ta_id = ta_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group_target_audience (
                id SERIAL PRIMARY KEY,
                ads_group_id INTEGER NOT NULL,
                ta_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ads_group_id) REFERENCES ads_group(ads_group_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (ta_id) REFERENCES target_audience(ta_id)
                    ON DELETE CASCADE,
                UNIQUE(ads_group_id, ta_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group_target_audience (ads_group_id, ta_id)
            VALUES (%s, %s)
            RETURNING id
            ''', (self.ads_group_id, self.ta_id))
            self.id = cursor.fetchone()[0]
            conn.commit()
            return self.id

    @staticmethod
    def get_by_ads_group_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, ads_group_id, ta_id 
            FROM ads_group_target_audience 
            WHERE ads_group_id = %s AND active = TRUE
            ''', (ads_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(ads_group_id, ta_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_group_target_audience 
            SET active = FALSE 
            WHERE ads_group_id = %s AND ta_id = %s
            ''', (ads_group_id, ta_id))
            conn.commit() 