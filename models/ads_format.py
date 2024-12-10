from configs.db import get_db_connection


class AdsFormat:
    def __init__(self, format_id=None, campaign_type_id=None, format_name="",
                 created_at=None, updated_at=None, status=True):
        self.format_id = format_id
        self.campaign_type_id = campaign_type_id
        self.format_name = format_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status

    def __str__(self):
        return f"AdsFormat(Type ID: {self.ads_type_id}, Format ID: {self.format_id}, Name: {self.format_name})"

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_format (
                format_id SERIAL PRIMARY KEY,
                campaign_type_id INTEGER NOT NULL,
                format_name VARCHAR(100),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (campaign_type_id) REFERENCES campaign_type(camp_type_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_format (campaign_type_id, format_name) 
            VALUES (%s, %s)
            ''', (self.campaign_type_id, self.format_name))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT campaign_type_id, format_id, format_name, created_at, updated_at, active 
                FROM ads_format
                WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ads_format
                SET ads_type_id = ?, ten_dinh_dang = ?
                WHERE format_id = ?
                ''', (self.campaign_type_id, self.format_name, self.format_id))
            conn.commit()

    @staticmethod
    def delete_by_id(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE ads_format SET active = false WHERE format_id = %s', (format_id,))
            conn.commit()
