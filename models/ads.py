from configs.db import get_db_connection


class Ads:
    def __init__(self, ads_id=None, ads_group_id=None, ads_status_id=None,
                 ten_tin_quang_cao="", URL_dich="", tong_chi_phi=0.0,
                 luot_xem=0, luot_nhan=0, CTR=0.0, CPC=0.0, CPM=0.0,
                 so_luong_mua_hang=0, conversion_rate=0.0, CPS=0.0,
                 video_watches_at_25=0, video_watches_at_50=0,
                 video_watches_at_75=0, video_watches_at_100=0,
                 video_watches_at_3s=0):
        self.ads_id = ads_id
        self.ads_group_id = ads_group_id
        self.ads_status_id = ads_status_id
        self.ten_tin_quang_cao = ten_tin_quang_cao
        self.URL_dich = URL_dich
        self.tong_chi_phi = tong_chi_phi
        self.luot_xem = luot_xem
        self.luot_nhan = luot_nhan
        self.CTR = CTR
        self.CPC = CPC
        self.CPM = CPM
        self.so_luong_mua_hang = so_luong_mua_hang
        self.conversion_rate = conversion_rate
        self.CPS = CPS
        self.video_watches_at_3s = video_watches_at_3s
        self.video_watches_at_25 = video_watches_at_25
        self.video_watches_at_50 = video_watches_at_50
        self.video_watches_at_75 = video_watches_at_75
        self.video_watches_at_100 = video_watches_at_100

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads (
                ads_id SERIAL PRIMARY KEY,
                ads_group_id INTEGER NOT NULL,
                ads_status_id INTEGER,
                ten_tin_quang_cao VARCHAR(100),
                URL_dich TEXT,
                tong_chi_phi DECIMAL(15,2),
                luot_xem INTEGER DEFAULT 0,
                luot_nhan INTEGER DEFAULT 0,
                CTR DECIMAL(5,2) DEFAULT 0,
                CPC DECIMAL(10,2) DEFAULT 0,
                CPM DECIMAL(10,2) DEFAULT 0,
                so_luong_mua_hang INTEGER DEFAULT 0,
                conversion_rate DECIMAL(5,2) DEFAULT 0,
                CPS DECIMAL(10,2) DEFAULT 0,
                video_watches_at_3s INTEGER DEFAULT 0,
                video_watches_at_25 INTEGER DEFAULT 0,
                video_watches_at_50 INTEGER DEFAULT 0,
                video_watches_at_75 INTEGER DEFAULT 0,
                video_watches_at_100 INTEGER DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ads_group_id) REFERENCES ads_group(ads_group_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (ads_status_id) REFERENCES status_ads(status_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads (ads_group_id, ads_status_id, ten_tin_quang_cao, URL_dich, tong_chi_phi, luot_xem, luot_nhan, CTR, CPC, CPM, so_luong_mua_hang, conversion_rate, CPS, video_watches_at_25, video_watches_at_50, video_watches_at_75, video_watches_at_100, video_watches_at_3s) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.ads_group_id, self.ads_status_id, self.ten_tin_quang_cao, self.URL_dich, self.tong_chi_phi, self.luot_xem, self.luot_nhan, self.CTR, self.CPC, self.CPM, self.so_luong_mua_hang, self.conversion_rate, self.CPS, self.video_watches_at_25, self.video_watches_at_50, self.video_watches_at_75, self.video_watches_at_100))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    ads.ads_id, 
                    ads.ads_group_id, 
                    ads.ads_status_id, 
                    ads.ten_tin_quang_cao, 
                    ads.URL_dich, 
                    ads.tong_chi_phi, 
                    ads.luot_xem, 
                    ads.luot_nhan, 
                    ads.CTR, 
                    ads.CPC, 
                    ads.CPM, 
                    ads.so_luong_mua_hang, 
                    ads.conversion_rate, 
                    ads.CPS, 
                    ads.video_watches_at_25, 
                    ads.video_watches_at_50, 
                    ads.video_watches_at_75, 
                    ads.video_watches_at_100, 
                    ads.video_watches_at_3s, 
                    ag.ten_nhom AS ten_nhom, 
                    c.ten_chien_dich AS ten_chien_dich, 
                    af.format_name AS dinh_dang, 
                    w.domain_website AS ten_website, 
                    az.ten_vung_quang_cao AS ten_vung_quang_cao
                FROM ads
                LEFT JOIN ads_group ag ON ag.ads_group_id = ads.ads_group_id
                LEFT JOIN campaign c ON c.camp_id = ag.camp_id
                LEFT JOIN ads_group_website agw ON agw.ads_group_id = ag.ads_group_id
                LEFT JOIN website w ON w.website_id = agw.website_id
                LEFT JOIN ads_zone az ON az.website_id = w.website_id
                LEFT JOIN ads_link_format alf ON alf.ads_id = ads.ads_id
                LEFT JOIN ads_format af ON af.format_id = alf.format_id;
            ''')

            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads
            SET ads_group_id = %s, ads_status_id = %s, ten_tin_quang_cao = %s, URL_dich = %s, tong_chi_phi = %s, luot_xem = %s, luot_nhan = %s, CTR = %s, CPC = %s, CPM = %s, so_luong_mua_hang = %s, conversion_rate = %s, CPS = %s, video_watches_at_25 = %s, video_watches_at_50 = %s, video_watches_at_75 = %s, video_watches_at_100 = %s, video_watches_at_3s = %s
            WHERE ads_id = %s
            ''', (self.ads_group_id, self.ads_status_id, self.ten_tin_quang_cao, self.URL_dich, self.tong_chi_phi, self.luot_xem, self.luot_nhan, self.CTR, self.CPC, self.CPM, self.so_luong_mua_hang, self.conversion_rate, self.CPS, self.video_watches_at_25, self.video_watches_at_50, self.video_watches_at_75, self.video_watches_at_100, self.ads_id))
            conn.commit()

    @staticmethod
    def delete_by_id(ads_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM ads WHERE ads_id = %s', (ads_id,))
            conn.commit()

    @staticmethod
    def get_ads_list():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT 
                    a.ads_id,
                    a.ten_tin_quang_cao,
                    ag.ten_nhom,
                    c.ten_chien_dich,
                    af.format_name as dinh_dang,
                    a.url_dich,
                    sa.ten_trang_thai as trang_thai,
                    a.tong_chi_phi,
                    a.luot_xem,
                    a.luot_nhan,
                    CASE 
                        WHEN a.luot_xem > 0 
                        THEN CAST(((a.luot_nhan::float / a.luot_xem) * 100) AS DECIMAL(10,2))
                        ELSE 0 
                    END as ctr,
                    CASE 
                        WHEN a.luot_nhan > 0 
                        THEN CAST((a.tong_chi_phi::float / a.luot_nhan) AS DECIMAL(10,2))
                        ELSE 0 
                    END as cpc,
                    CASE 
                        WHEN a.luot_xem > 0 
                        THEN CAST((a.tong_chi_phi::float / a.luot_xem) * 1000 AS DECIMAL(10,2))
                        ELSE 0 
                    END as cpm,
                    a.so_luong_mua_hang,
                    CASE 
                        WHEN a.luot_nhan > 0 
                        THEN CAST((a.so_luong_mua_hang::float / a.luot_nhan) * 100 AS DECIMAL(10,2))
                        ELSE 0 
                    END as ti_le_chuyen_doi,
                    CASE 
                        WHEN a.so_luong_mua_hang > 0 
                        THEN CAST((a.tong_chi_phi::float / a.so_luong_mua_hang) AS DECIMAL(10,2))
                        ELSE 0 
                    END as cps,
                    a.video_watches_at_3s as video_view_3s,
                    a.active as dang_hien_thi,
                    az.ten_vung_quang_cao
                FROM ads a
                LEFT JOIN ads_group ag ON ag.ads_group_id = a.ads_group_id
                LEFT JOIN campaign c ON c.camp_id = ag.camp_id
                LEFT JOIN ads_group_website agw ON agw.ads_group_id = ag.ads_group_id
                LEFT JOIN website w ON w.website_id = agw.website_id
                LEFT JOIN ads_zone az ON az.website_id = w.website_id
                LEFT JOIN ads_link_format alf ON alf.ads_id = a.ads_id
                LEFT JOIN ads_format af ON af.format_id = alf.format_id
                LEFT JOIN status_ads sa ON sa.status_id = a.ads_status_id
                WHERE a.active = true
                AND ag.active = true
                AND agw.active = true
                ORDER BY a.created_at DESC
            '''
            cursor.execute(query)
            return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    @staticmethod
    def update_ads_status(ads_id, active):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = '''
                UPDATE ads
                SET active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE ads_id = %s
                RETURNING ads_id
            '''
            cursor.execute(query, (active, ads_id))
            conn.commit()
            return cursor.fetchone() is not None
