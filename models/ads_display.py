from configs.db import get_db_connection


class AdsDisplay:
    def __init__(self, ads_id=None, format_id=None, dang_tai_tep_anh="",
                 tieu_de="", noi_dung=""):
        self.ads_id = ads_id
        self.format_id = format_id
        self.dang_tai_tep_anh = dang_tai_tep_anh
        self.tieu_de = tieu_de
        self.noi_dung = noi_dung

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_display (
                ads_id SERIAL PRIMARY KEY,
                format_id INTEGER,
                dang_tai_tep_anh BYTEA,
                tieu_de TEXT,
                noi_dung TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_display (
                format_id, dang_tai_tep_anh, tieu_de, noi_dung
            )
            VALUES (%s, %s, %s, %s)
            RETURNING ads_id
            ''', (
                self.format_id, self.dang_tai_tep_anh,
                self.tieu_de, self.noi_dung
            ))
            self.ads_id = cursor.fetchone()[0]
            conn.commit()
            return self.ads_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT ad.*, f.ten_format 
            FROM ads_display ad
            LEFT JOIN format f ON ad.format_id = f.format_id
            WHERE ad.active = TRUE
            ORDER BY ad.created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(ads_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM ads_display WHERE ads_id = %s AND active = TRUE', (ads_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def update(ads_id, data={}):
        with get_db_connection() as conn:
            cursor = conn.cursor()

            update_fields = []
            params = []

            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)

            if update_fields:
                query = f'''
                UPDATE ads_display 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE ads_id = %s AND active = TRUE
                '''
                params.append(ads_id)

                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(ads_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_display SET active = FALSE WHERE ads_id = %s
            ''', (ads_id,))
            conn.commit()
