from configs.db import get_db_connection


class AdsGroup:
    def __init__(self, ads_group_id=None, camp_id=None, ads_group_status_id=None,
                 ten_nhom="", nham_chon_all_san_pham=False, nham_chon_doi_tuong=False,
                 nham_chon_dia_ly="", gioi_tinh_khong_xac_dinh=False,
                 gioi_tinh_nam=False, gioi_tinh_nu=False,
                 tuoi_less_than_18=False, tuoi_from_18_to_24=False,
                 tuoi_from_25_to_34=False, tuoi_from_35_to_50=False,
                 tuoi_more_than_50=False, created_at=None, updated_at=None,
                 active=True):
        self.ads_group_id = ads_group_id
        self.camp_id = camp_id
        self.ads_group_status_id = ads_group_status_id
        self.ten_nhom = ten_nhom
        self.nham_chon_all_san_pham = nham_chon_all_san_pham
        self.nham_chon_doi_tuong = nham_chon_doi_tuong
        self.nham_chon_dia_ly = nham_chon_dia_ly
        self.gioi_tinh_khong_xac_dinh = gioi_tinh_khong_xac_dinh
        self.gioi_tinh_nam = gioi_tinh_nam
        self.gioi_tinh_nu = gioi_tinh_nu
        self.tuoi_less_than_18 = tuoi_less_than_18
        self.tuoi_from_18_to_24 = tuoi_from_18_to_24
        self.tuoi_from_25_to_34 = tuoi_from_25_to_34
        self.tuoi_from_35_to_50 = tuoi_from_35_to_50
        self.tuoi_more_than_50 = tuoi_more_than_50
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_group (
                ads_group_id SERIAL PRIMARY KEY,
                camp_id INTEGER NOT NULL,
                ads_group_status_id INTEGER NOT NULL,
                ten_nhom VARCHAR(100),
                ngan_sach_ngay DECIMAL(15,2) DEFAULT 0,
                tong_chi_phi DECIMAL(15,2) DEFAULT 0,
                luot_xem INTEGER DEFAULT 0,
                luot_nhan INTEGER DEFAULT 0,
                ctr DECIMAL(5,2) DEFAULT 0,
                cpc DECIMAL(10,2) DEFAULT 0,
                cpm DECIMAL(10,2) DEFAULT 0,
                so_luong_mua_hang INTEGER DEFAULT 0,
                conversion_rate DECIMAL(5,2) DEFAULT 0,
                cps DECIMAL(10,2) DEFAULT 0,
                videoview3s INTEGER DEFAULT 0,
                videowatchesat25 INTEGER DEFAULT 0,
                videowatchesat50 INTEGER DEFAULT 0,
                videowatchesat75 INTEGER DEFAULT 0,
                videowatchesat100 INTEGER DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (camp_id) REFERENCES campaign(camp_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (ads_group_status_id) REFERENCES ads_group_status(ads_group_status_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ads_group (camp_id, ads_group_status_id, ten_nhom, nham_chon_all_san_pham, nham_chon_doi_tuong, nham_chon_dia_ly, gioi_tinh_khong_xac_dinh, gioi_tinh_nam, gioi_tinh_nu, tuoi_less_than_18, tuoi_from_18_to_24, tuoi_from_25_to_34, tuoi_from_35_to_50, tuoi_more_than_50)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.camp_id, self.ads_group_status_id, self.ten_nhom,
                  self.nham_chon_all_san_pham, self.nham_chon_doi_tuong, self.nham_chon_dia_ly,
                  self.gioi_tinh_khong_xac_dinh, self.gioi_tinh_nam, self.gioi_tinh_nu,
                  self.tuoi_less_than_18, self.tuoi_from_18_to_24, self.tuoi_from_25_to_34,
                  self.tuoi_from_35_to_50, self.tuoi_more_than_50))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ag.ads_group_id, ag.ten_nhom, c.ten_chi_tieu, ags.ten_trang_thai, at.ten_loai_quang_cao, 
                       ag.tong_chi_phi, ag.luot_xem, ag.luot_nhan, ag.ctr, ag.cpc, ag.cpm, 
                       ag.so_luong_mua_hang as sl_mua_hang, 
                       ag.conversion_rate as percent_chuyen_doi_mua_hang,
                       ag.cps, ag.video_view_3s,
                       CONCAT(ag.bat_dau, ' - ', ag.ket_thuc) as bat_dau_ket_thuc
                FROM ads_group ag
                LEFT JOIN campaign c ON ag.camp_id = c.camp_id 
                LEFT JOIN ads_group_status ags ON ag.ads_group_status_id = ags.ads_group_status_id
                WHERE ag.active = true
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
                SELECT ag.ads_group_id, ag.ten_nhom, c.ten_chi_tieu, ags.ten_trang_thai, at.ten_loai_quang_cao, 
                       ag.tong_chi_phi, ag.luot_xem, ag.luot_nhan, ag.ctr, ag.cpc, ag.cpm, 
                       ag.so_luong_mua_hang, ag.conversion_rate, ag.cps, ag.video_view_3s, 
                       ag.video_watches_25, ag.video_watches_50, ag.video_watches_75, ag.video_watches_100, 
                       ag.product_group_id, ag.ta_id, ag.nham_chon_dia_ly, ag.nham_chon_gioi_tinh, 
                       ag.nham_chon_do_tuoi, ag.website_id, ag.active
                FROM ads_group ag
                LEFT JOIN campaign c ON ag.camp_id = c.camp_id
                LEFT JOIN ads_group_status ags ON ag.ads_group_status_id = ags.ads_group_status_id
                WHERE ag.ads_group_id = %s
            ''', (ads_group_id,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row))

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ads_group
            SET camp_id = ?, ads_group_status_id = ?, ten_nhom = ?, nham_chon_all_san_pham = ?, nham_chon_doi_tuong = ?, nham_chon_dia_ly = ?, gioi_tinh_khong_xac_dinh = ?, gioi_tinh_nam = ?, gioi_tinh_nu = ?, tuoi_less_than_18 = ?, tuoi_from_18_to_24 = ?, tuoi_from_25_to_34 = ?, tuoi_from_35_to_50 = ?, tuoi_more_than_50 = ?
            WHERE ads_group_id = ?
            ''', (
                self.camp_id, self.ads_group_status_id, self.ten_nhom,
                self.nham_chon_all_san_pham, self.nham_chon_doi_tuong, self.nham_chon_dia_ly,
                self.gioi_tinh_khong_xac_dinh, self.gioi_tinh_nam, self.gioi_tinh_nu,
                self.tuoi_less_than_18, self.tuoi_from_18_to_24, self.tuoi_from_25_to_34,
                self.tuoi_from_35_to_50, self.tuoi_more_than_50, self.ads_group_id))
            conn.commit()

    @staticmethod
    def delete_by_id(ads_group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ads_group SET active = 0 WHERE ads_group_id = ?
            ''', (ads_group_id,))
            conn.commit()
