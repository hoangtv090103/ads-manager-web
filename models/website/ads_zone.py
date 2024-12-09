from configs.db import get_db_connection

class AdsZone:
    def __init__(self, zone_id=None, website_id=None, ten_vung_quang_cao="",
                 size_id=None, ma_nhung_vung_quang_cao=""):
        self.zone_id = zone_id
        self.website_id = website_id
        self.ten_vung_quang_cao = ten_vung_quang_cao
        self.size_id = size_id
        self.ma_nhung_vung_quang_cao = ma_nhung_vung_quang_cao

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_zone (
                zone_id SERIAL PRIMARY KEY,
                website_id INTEGER NOT NULL,
                ten_vung_quang_cao VARCHAR(100),
                size_id INTEGER NOT NULL,
                ma_nhung_vung_quang_cao TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (size_id) REFERENCES ads_zone_size(size_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_zone (website_id, ten_vung_quang_cao, size_id, ma_nhung_vung_quang_cao) 
            VALUES (?, ?, ?, ?)
            ''', (self.website_id, self.ten_vung_quang_cao, self.size_id, self.ma_nhung_vung_quang_cao))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT website_id, ten_vung_quang_cao, size_id, ma_nhung_vung_quang_cao FROM ads_zone
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone
            SET website_id = ?, ten_vung_quang_cao = ?, size_id = ?, ma_nhung_vung_quang_cao = ?
            WHERE zone_id = ?
            ''', (self.website_id, self.ten_vung_quang_cao, self.size_id, self.ma_nhung_vung_quang_cao, self.zone_id))
            conn.commit()

    @staticmethod
    def delete_by_id(zone_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone SET active = 0 WHERE zone_id = ?
            ''', (zone_id,))
            conn.commit()
