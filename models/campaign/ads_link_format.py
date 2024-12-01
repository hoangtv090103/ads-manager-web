class AdsLinkFormat:
    def __init__(self, ads_id=None, format_id=None):
        self.ads_id = ads_id
        self.format_id = format_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_link_format (
                ads_id INTEGER,
                format_id INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ads_id, format_id),
                FOREIGN KEY (ads_id) REFERENCES ads(ads_id),
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
            )
            ''')
            conn.commit() 