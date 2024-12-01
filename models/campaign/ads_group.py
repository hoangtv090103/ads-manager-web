from configs.db import get_db_connection


class AdsGroup:
    def __init__(self, ads_group_id=None, camp_id=None, ads_group_status_id=None, ads_type_id=None, ten_nhom="",
                 tong_chi_phi=0.0, luot_xem=0, luot_nhan=0, ctr=0.0, cpc=0.0, cpm=0.0, so_luong_mua_hang=0,
                 conversion_rate=0.0, cps=0.0, video_view_3s=0, video_watches_25=0, video_watches_50=0,
                 video_watches_75=0, video_watches_100=0, product_group_id=None, ta_id=None, nham_chon_dia_ly="",
                 nham_chon_gioi_tinh="", nham_chon_do_tuoi="", website_id=None):
        self.ads_group_id = ads_group_id
        self.camp_id = camp_id
        self.ads_group_status_id = ads_group_status_id
        self.ads_type_id = ads_type_id
        self.ten_nhom = ten_nhom
        self.tong_chi_phi = tong_chi_phi
        self.luot_xem = luot_xem
        self.luot_nhan = luot_nhan
        self.ctr = ctr
        self.cpc = cpc
        self.cpm = cpm
        self.so_luong_mua_hang = so_luong_mua_hang
        self.conversion_rate = conversion_rate
        self.cps = cps
        self.video_view_3s = video_view_3s
        self.video_watches_25 = video_watches_25
        self.video_watches_50 = video_watches_50
        self.video_watches_75 = video_watches_75
        self.video_watches_100 = video_watches_100
        self.product_group_id = product_group_id
        self.ta_id = ta_id
        self.nham_chon_dia_ly = nham_chon_dia_ly
        self.nham_chon_gioi_tinh = nham_chon_gioi_tinh
        self.nham_chon_do_tuoi = nham_chon_do_tuoi
        self.website_id = website_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group (
                ads_group_id SERIAL PRIMARY KEY,
                camp_id INTEGER,
                ads_group_status_id INTEGER,
                ads_type_id INTEGER,
                ten_nhom VARCHAR(50),
                tong_chi_phi FLOAT,
                luot_xem INTEGER,
                luot_nhan INTEGER,
                ctr FLOAT,
                cpc FLOAT,
                cpm FLOAT,
                so_luong_mua_hang INTEGER,
                conversion_rate FLOAT,
                cps FLOAT,
                video_view_3s INTEGER,
                video_watches_25 INTEGER,
                video_watches_50 INTEGER,
                video_watches_75 INTEGER,
                video_watches_100 INTEGER,
                product_group_id INTEGER,
                ta_id INTEGER,
                nham_chon_dia_ly VARCHAR(30),
                nham_chon_gioi_tinh VARCHAR(10),
                nham_chon_do_tuoi VARCHAR(20),
                website_id INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (camp_id) REFERENCES campaign(camp_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (ads_group_status_id) REFERENCES ads_group_status(ads_group_status_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (ads_type_id) REFERENCES ads_type(ads_type_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (product_group_id) REFERENCES product_group(group_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (ta_id) REFERENCES target_audience(ta_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group (camp_id, ads_group_status_id, ads_type_id, ten_nhom, tong_chi_phi, luot_xem, luot_nhan, ctr, cpc, cpm, so_luong_mua_hang, conversion_rate, cps, video_view_3s, video_watches_25, video_watches_50, video_watches_75, video_watches_100, product_group_id, ta_id, nham_chon_dia_ly, nham_chon_gioi_tinh, nham_chon_do_tuoi, website_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.camp_id, self.ads_group_status_id, self.ads_type_id, self.ten_nhom,
                  self.tong_chi_phi, self.luot_xem, self.luot_nhan, self.ctr, self.cpc, self.cpm,
                  self.so_luong_mua_hang, self.conversion_rate, self.cps, self.video_view_3s, self.video_watches_25,
                  self.video_watches_50, self.video_watches_75, self.video_watches_100, self.product_group_id,
                  self.ta_id, self.nham_chon_dia_ly, self.nham_chon_gioi_tinh, self.nham_chon_do_tuoi, self.website_id))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ag.ads_group_id, ag.ten_nhom, ags.ten_trang_thai, at.ten_loai_quang_cao, ag.tong_chi_phi, ag.luot_xem, ag.luot_nhan, ag.ctr, ag.cpc, ag.cpm, ag.so_luong_mua_hang, ag.conversion_rate, ag.cps, ag.video_view_3s, ag.video_watches_25, ag.video_watches_50, ag.video_watches_75, ag.video_watches_100, ag.product_group_id, ag.ta_id, ag.nham_chon_dia_ly, ag.nham_chon_gioi_tinh, ag.nham_chon_do_tuoi, ag.website_id, ag.active
                FROM ads_group ag
                LEFT JOIN campaign c ON ag.camp_id = c.camp_id
                LEFT JOIN ads_group_status ags ON ag.ads_group_status_id = ags.ads_group_status_id
                LEFT JOIN ads_type at ON ag.ads_type_id = at.ads_type_id
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
 SELECT ag.ads_group_id, ag.ten_nhom, c.ten_chi_tieu, ags.ten_trang_thai, at.ten_loai_quang_cao, ag.tong_chi_phi, ag.luot_xem, ag.luot_nhan, ag.ctr, ag.cpc, ag.cpm, ag.so_luong_mua_hang, ag.conversion_rate, ag.cps, ag.video_view_3s, ag.video_watches_25, ag.video_watches_50, ag.video_watches_75, ag.video_watches_100, ag.product_group_id, ag.ta_id, ag.nham_chon_dia_ly, ag.nham_chon_gioi_tinh, ag.nham_chon_do_tuoi, ag.website_id, ag.active
                FROM ads_group ag
                LEFT JOIN campaign c ON ag.camp_id = c.camp_id
                LEFT JOIN ads_group_status ags ON ag.ads_group_status_id = ags.ads_group_status_id
                LEFT JOIN ads_type at ON ag.ads_type_id = at.ads_type_id
                WHERE ag.ads_group_id = %s
            ''', (ads_group_id,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row))

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_group
            SET camp_id = ?, ads_group_status_id = ?, ads_type_id = ?, ten_nhom = ?, tong_chi_phi = ?, luot_xem = ?, luot_nhan = ?, ctr = ?, cpc = ?, cpm = ?, so_luong_mua_hang = ?, conversion_rate = ?, cps = ?, video_view_3s = ?, video_watches_25 = ?, video_watches_50 = ?, video_watches_75 = ?, video_watches_100 = ?, product_group_id = ?, ta_id = ?, nham_chon_dia_ly = ?, nham_chon_gioi_tinh = ?, nham_chon_do_tuoi = ?, website_id = ?
            WHERE ads_group_id = ?
            ''', (
                self.camp_id, self.ads_group_status_id, self.ads_type_id, self.ten_nhom, self.tong_chi_phi,
                self.luot_xem,
                self.luot_nhan, self.ctr, self.cpc, self.cpm, self.so_luong_mua_hang, self.conversion_rate, self.cps,
                self.video_view_3s, self.video_watches_25, self.video_watches_50, self.video_watches_75,
                self.video_watches_100, self.product_group_id, self.ta_id, self.nham_chon_dia_ly,
                self.nham_chon_gioi_tinh,
                self.nham_chon_do_tuoi, self.website_id, self.ads_group_id))
            conn.commit()

    @staticmethod
    def delete_by_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ads_group SET active = 0 WHERE ads_group_id = ?
            ''', (ads_group_id,))
            conn.commit()
