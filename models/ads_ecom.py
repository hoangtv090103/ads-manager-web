from configs.db import get_db_connection
class AdsEcom:
    def __init__(self, ads_id=None, format_id=None, anh_banner_chan_trang="", 
                 video_banner="", anh_thumbnail="", su_dung_mau_banner_co_san=False,
                 ten_san_pham="", hien_thi_gia_khuyen_mai=False, 
                 hien_thi_freeship_sp=False):
        self.ads_id = ads_id
        self.format_id = format_id
        self.anh_banner_chan_trang = anh_banner_chan_trang
        self.video_banner = video_banner
        self.anh_thumbnail = anh_thumbnail
        self.su_dung_mau_banner_co_san = su_dung_mau_banner_co_san
        self.ten_san_pham = ten_san_pham
        self.hien_thi_gia_khuyen_mai = hien_thi_gia_khuyen_mai
        self.hien_thi_freeship_sp = hien_thi_freeship_sp

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_ecom (
                ads_id INTEGER PRIMARY KEY,
                format_id INTEGER NOT NULL,
                anh_banner_chan_trang VARCHAR(255),
                video_banner VARCHAR(255),
                anh_thumbnail VARCHAR(255),
                su_dung_mau_banner_co_san BOOLEAN DEFAULT FALSE,
                ten_san_pham VARCHAR(100),
                hien_thi_gia_khuyen_mai BOOLEAN DEFAULT FALSE,
                hien_thi_freeship_sp BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
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
            INSERT INTO ads_ecom (
                ads_id, format_id, anh_banner_chan_trang, video_banner,
                anh_thumbnail, su_dung_mau_banner_co_san, ten_san_pham,
                hien_thi_gia_khuyen_mai, hien_thi_freeship_sp
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING ads_id
            ''', (
                self.ads_id, self.format_id, self.anh_banner_chan_trang,
                self.video_banner, self.anh_thumbnail, 
                self.su_dung_mau_banner_co_san, self.ten_san_pham,
                self.hien_thi_gia_khuyen_mai, self.hien_thi_freeship_sp
            ))
            self.ads_id = cursor.fetchone()[0]
            conn.commit()
            return self.ads_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT ae.*, f.ten_format 
            FROM ads_ecom ae
            LEFT JOIN format f ON ae.format_id = f.format_id
            WHERE ae.active = TRUE
            ORDER BY ae.created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(ads_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ads_ecom WHERE ads_id = %s AND active = TRUE', (ads_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_product_name(ten_san_pham):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM ads_ecom WHERE ten_san_pham ILIKE %s AND active = TRUE', 
                (f'%{ten_san_pham}%',)
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
                UPDATE ads_ecom 
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
            UPDATE ads_ecom SET active = FALSE WHERE ads_id = %s
            ''', (ads_id,))
            conn.commit()