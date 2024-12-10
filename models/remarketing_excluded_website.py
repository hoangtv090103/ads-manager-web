from configs.db import get_db_connection


class RemarketingExcludedWebsite:
    def __init__(self, remarketing_id=None, website_id=None):
        self.remarketing_id = remarketing_id
        self.website_id = website_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS remarketing_excluded_website (
                remarketing_id INTEGER,
                website_id INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (remarketing_id, website_id),
                FOREIGN KEY (website_id) REFERENCES website(website_id) ON DELETE CASCADE,
                FOREIGN KEY (remarketing_id) REFERENCES remarketing_setting(remarketing_id) ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO remarketing_excluded_website (remarketing_id, website_id)
            VALUES (%s, %s)
            ''', (self.remarketing_id, self.website_id))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT rew.remarketing_id, rew.website_id,
                       w.ten_website, w.url, w.website_status_id,
                       rew.created_at, rew.updated_at
                FROM remarketing_excluded_website rew
                JOIN website w ON rew.website_id = w.website_id
                WHERE rew.active = TRUE
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_remarketing_id(remarketing_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT rew.remarketing_id, rew.website_id,
                       w.ten_website, w.url, w.website_status_id,
                       rew.created_at, rew.updated_at
                FROM remarketing_excluded_website rew
                JOIN website w ON rew.website_id = w.website_id
                WHERE rew.remarketing_id = %s AND rew.active = TRUE
            ''', (remarketing_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(remarketing_id, website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE remarketing_excluded_website 
            SET active = FALSE 
            WHERE remarketing_id = %s AND website_id = %s
            ''', (remarketing_id, website_id))
            conn.commit()
