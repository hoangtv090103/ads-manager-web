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

    @staticmethod
    def get_by_id(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ads_format WHERE format_id = %s
            ''', (format_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_campaign_type_id(campaign_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ads_format WHERE campaign_type_id = %s
            ''', (campaign_type_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_size_id(size_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT
                    af.format_id,
                    af.format_name,
                    ct.camp_type_id,
                    ct.ten_loai_chien_dich,
                    azs.ten_kich_thuoc
                FROM ads_format af
                LEFT JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                LEFT JOIN ad_size_format asf ON af.format_id = asf.format_id
                LEFT JOIN ads_zone_size azs ON asf.size_id = azs.size_id
                WHERE asf.size_id = %s 
                    AND asf.active = true 
                    AND af.active = true
                    AND ct.active = true
                    AND azs.active = true
                ORDER BY 
                    ct.ten_loai_chien_dich,
                    af.format_name
            ''', (size_id,))
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([
                'format_id', 
                'format_name',
                'campaign_type_id', 
                'ten_loai_chien_dich',
                'ten_kich_thuoc'
            ], row)) for row in rows]

    @staticmethod
    def get_by_name(format_name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ads_format WHERE format_name ILIKE     %s
            ''', (format_name,))
            rows = cursor.fetchone()
            if not rows:
                return None
            return dict(zip([column[0] for column in cursor.description], rows))

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
