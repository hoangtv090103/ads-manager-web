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
                ads_status_id INTEGER NOT NULL,
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
                SELECT ads_id, ads_group_id, ads_status_id, ten_tin_quang_cao, URL_dich, tong_chi_phi, luot_xem, luot_nhan, CTR, CPC, CPM, so_luong_mua_hang, conversion_rate, CPS, video_watches_at_25, video_watches_at_50, video_watches_at_75, video_watches_at_100, video_watches_at_3s FROM ads
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
