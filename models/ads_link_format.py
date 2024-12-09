from configs.db import get_db_connection


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
                active BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (ads_id, format_id),
                FOREIGN KEY (ads_id) REFERENCES ads(ads_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_link_format (ads_id, format_id)
            VALUES (%s, %s)
            ''', (self.ads_id, self.format_id))
            conn.commit()

    @staticmethod
    def get_by_ads_id(ads_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT alf.*, f.format_name
            FROM ads_link_format alf
            LEFT JOIN format f ON alf.format_id = f.format_id
            WHERE alf.ads_id = %s AND alf.active = TRUE
            ''', (ads_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(ads_id, format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_link_format 
            SET active = FALSE 
            WHERE ads_id = %s AND format_id = %s
            ''', (ads_id, format_id))
            conn.commit() 