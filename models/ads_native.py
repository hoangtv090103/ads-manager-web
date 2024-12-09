from configs.db import get_db_connection



class AdsNative:
    def __init__(self, ads_id=None, format_id=None, video="", anh_thumbnail="",
                 logo="", anh_quang_cao="", ten_brand="", tieu_de="",
                 noi_dung="", nut_cta=None, noi_dung_cta="", url_cta=""):
        self.ads_id = ads_id
        self.format_id = format_id
        self.video = video
        self.anh_thumbnail = anh_thumbnail
        self.logo = logo
        self.anh_quang_cao = anh_quang_cao
        self.ten_brand = ten_brand
        self.tieu_de = tieu_de
        self.noi_dung = noi_dung
        self.nut_cta = nut_cta
        self.noi_dung_cta = noi_dung_cta
        self.url_cta = url_cta

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_native (
                ads_id SERIAL PRIMARY KEY,
                format_id INTEGER,
                video VARCHAR(255),
                anh_thumbnail VARCHAR(255),
                logo VARCHAR(255),
                anh_quang_cao VARCHAR(255),
                ten_brand VARCHAR(255),
                tieu_de TEXT,
                noi_dung TEXT,
                nut_cta INTEGER,
                noi_dung_cta TEXT,
                url_cta TEXT,
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
            INSERT INTO ads_native (
                format_id, video, anh_thumbnail, logo, anh_quang_cao,
                ten_brand, tieu_de, noi_dung, nut_cta, noi_dung_cta, url_cta
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING ads_id
            ''', (
                self.format_id, self.video, self.anh_thumbnail, self.logo,
                self.anh_quang_cao, self.ten_brand, self.tieu_de, self.noi_dung,
                self.nut_cta, self.noi_dung_cta, self.url_cta
            ))
            self.ads_id = cursor.fetchone()[0]
            conn.commit()
            return self.ads_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT an.*, f.ten_format 
            FROM ads_native an
            LEFT JOIN format f ON an.format_id = f.format_id
            WHERE an.active = TRUE
            ORDER BY an.created_at DESC
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
                'SELECT * FROM ads_native WHERE ads_id = %s AND active = TRUE', (ads_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_brand_name(ten_brand):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM ads_native WHERE ten_brand ILIKE %s AND active = TRUE',
                (f'%{ten_brand}%',)
            )
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

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
                UPDATE ads_native 
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
            UPDATE ads_native SET active = FALSE WHERE ads_id = %s
            ''', (ads_id,))
            conn.commit()
