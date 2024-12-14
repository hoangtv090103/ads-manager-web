from configs.db import get_db_connection

class AdsZoneFormat:
    def __init__(self, zone_id=None, format_id=None):
        self.zone_id = zone_id
        self.format_id = format_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_zone_format (
                zone_id INTEGER NOT NULL,
                format_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (zone_id, format_id),
                FOREIGN KEY (zone_id) REFERENCES ads_zone(zone_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_zone_format (zone_id, format_id)
            VALUES (%s, %s)
            ''', (self.zone_id, self.format_id))
            conn.commit()

    @staticmethod
    def get_by_zone_id(zone_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT azf.*, af.format_name, ct.ten_loai_chien_dich
            FROM ads_zone_format azf
            JOIN ads_format af ON azf.format_id = af.format_id
            JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
            WHERE azf.zone_id = %s AND azf.active = true
            ''', (zone_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone_format 
            SET active = false 
            WHERE zone_id = %s AND format_id = %s
            ''', (self.zone_id, self.format_id))
            conn.commit() 