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
                remarketing_id INTEGER NOT NULL,
                website_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (remarketing_id, website_id),
                FOREIGN KEY (remarketing_id) REFERENCES remarketing_setting(remarketing_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit() 