from configs.db import get_db_connection

class AdsGroupWebsite:
    def __init__(self, id=None, ads_group_id=None, website_id=None):
        self.id = id
        self.ads_group_id = ads_group_id
        self.website_id = website_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group_website (
                id SERIAL PRIMARY KEY,
                ads_group_id INTEGER NOT NULL,
                website_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ads_group_id) REFERENCES ads_group(ads_group_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE,
                UNIQUE(ads_group_id, website_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group_website (ads_group_id, website_id)
            VALUES (%s, %s)
            RETURNING id
            ''', (self.ads_group_id, self.website_id))
            self.id = cursor.fetchone()[0]
            conn.commit()
            return self.id

    @staticmethod
    def get_by_ads_group_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, ads_group_id, website_id 
            FROM ads_group_website 
            WHERE ads_group_id = %s AND active = TRUE
            ''', (ads_group_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_website_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, ads_group_id, website_id 
            FROM ads_group_website 
            WHERE website_id = %s AND active = TRUE
            ''', (website_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_group_website 
            SET active = FALSE 
            WHERE id = %s
            ''', (id,))
            conn.commit() 