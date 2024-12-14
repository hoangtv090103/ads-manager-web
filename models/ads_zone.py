from configs.db import get_db_connection

class AdsZone:
    def __init__(self, zone_id=None, website_id=None, ten_vung_quang_cao="",
                 size_id=None, ma_nhung_vung_quang_cao="", formats=None):
        self.zone_id = zone_id
        self.website_id = website_id
        self.ten_vung_quang_cao = ten_vung_quang_cao
        self.size_id = size_id
        self.ma_nhung_vung_quang_cao = ma_nhung_vung_quang_cao
        self.formats = formats or []

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
            try:
                # Bắt đầu transaction
                cursor.execute('BEGIN')
                
                # Insert vùng quảng cáo
                cursor.execute('''
                INSERT INTO ads_zone (
                    website_id, ten_vung_quang_cao, size_id, 
                    ma_nhung_vung_quang_cao
                ) 
                VALUES (%s, %s, %s, %s)
                RETURNING zone_id
                ''', (
                    self.website_id, self.ten_vung_quang_cao, 
                    self.size_id, self.ma_nhung_vung_quang_cao,
                ))
                
                self.zone_id = cursor.fetchone()[0]
                
                # Insert các định dạng được chọn
                if self.formats:
                    cursor.executemany('''
                    INSERT INTO ads_zone_format (zone_id, format_id)
                    VALUES (%s, %s)
                    ''', [(self.zone_id, format_id) for format_id in self.formats])
                
                # Commit transaction
                cursor.execute('COMMIT')
                return self.zone_id
                
            except Exception as e:
                cursor.execute('ROLLBACK')
                raise e

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT website_id, ten_vung_quang_cao, size_id, ma_nhung_vung_quang_cao FROM ads_zone
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
    @staticmethod
    def get_by_id(zone_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM ads_zone WHERE zone_id = %s
            ''', (zone_id,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row))
        
    @staticmethod
    def get_by_website_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM ads_zone WHERE website_id = %s
            ''', (website_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone
            SET website_id = %s, ten_vung_quang_cao = %s, size_id = %s, ma_nhung_vung_quang_cao = %s
            WHERE zone_id = %s
            ''', (self.website_id, self.ten_vung_quang_cao, self.size_id, self.ma_nhung_vung_quang_cao, self.zone_id))
            conn.commit()

    @staticmethod
    def delete_by_id(zone_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_zone SET active = 0 WHERE zone_id = %s
            ''', (zone_id,))
            conn.commit()
