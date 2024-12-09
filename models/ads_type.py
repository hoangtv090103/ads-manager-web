from configs.db import get_db_connection

class AdsType:
    def __init__(self, ads_type_id=None, ten_loai_quang_cao=""):
        self.ads_type_id = ads_type_id
        self.ten_loai_quang_cao = ten_loai_quang_cao

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_type (
                ads_type_id SERIAL PRIMARY KEY,
                ten_loai_quang_cao VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            # Insert default roles if they don't exist
            cursor.execute('SELECT COUNT(*) FROM ads_type')
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    '''
                    INSERT INTO ads_type (ten_loai_quang_cao) VALUES (%s)
                    ''',
                    [
                        ('ecommerce',),
                        ('display_ads',),
                        ('native_ads',)
                    ]
                )
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_type (ten_loai_quang_cao)
            VALUES (?)
            ''', (self.ten_loai_quang_cao,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ads_type_id, ten_loai_quang_cao, created_at, updated_at, active 
                FROM ads_type 
                WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_one(ads_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ads_type_id, ten_loai_quang_cao 
                FROM ads_type 
                WHERE ads_type_id=? AND active=1 LIMIT 1
            ''', (ads_type_id,))
            ads_type = cursor.fetchone()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in ads_type]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_type
            SET ten_loai_quang_cao = ?, updated_at = CURRENT_TIMESTAMP
            WHERE ads_type_id = ?
            ''', (self.ten_loai_quang_cao, self.ads_type_id))
            conn.commit()

    @staticmethod
    def delete_by_id(ads_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE ads_type SET active = 0 WHERE ads_type_id = ?', (ads_type_id,))
            conn.commit()

    def __str__(self):
        return f"AdsType(ID: {self.ads_type_id}, Name: {self.ten_loai_quang_cao})"
