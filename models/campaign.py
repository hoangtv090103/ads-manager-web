from configs.db import get_db_connection


class Campaign:
    def __init__(self, camp_id=None, ten_chien_dich="", camp_type_id=None,
                 campstatus_id=None, source_id=None, ngan_sach_ngay=0,
                 tong_chi_phi=0, luot_xem=0, luot_nhan=0, ctr=0, cpc=0,
                 cpm=0, so_luong_mua_hang=0, conversion_rate=0, cps=0,
                 videoview3s=0, videowatchesat25=0, videowatchesat50=0,
                 videowatchesat75=0, videowatchesat100=0, ngay_bat_dau=None,
                 ngay_ket_thuc=None, created_at=None, updated_at=None, active=True):
        self.camp_id = camp_id
        self.ten_chien_dich = ten_chien_dich
        self.camp_type_id = camp_type_id
        self.campstatus_id = campstatus_id
        self.source_id = source_id
        self.ngan_sach_ngay = ngan_sach_ngay
        self.tong_chi_phi = tong_chi_phi
        self.luot_xem = luot_xem
        self.luot_nhan = luot_nhan
        self.ctr = ctr
        self.cpc = cpc
        self.cpm = cpm
        self.so_luong_mua_hang = so_luong_mua_hang
        self.conversion_rate = conversion_rate
        self.cps = cps
        self.videoview3s = videoview3s
        self.videowatchesat25 = videowatchesat25
        self.videowatchesat50 = videowatchesat50
        self.videowatchesat75 = videowatchesat75
        self.videowatchesat100 = videowatchesat100
        self.ngay_bat_dau = ngay_bat_dau
        self.ngay_ket_thuc = ngay_ket_thuc
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign (
                camp_id SERIAL PRIMARY KEY,
                ten_chien_dich VARCHAR(255),
                camp_type_id INTEGER,
                campstatus_id INTEGER,
                source_id INTEGER,
                ngan_sach_ngay FLOAT,
                tong_chi_phi FLOAT,
                luot_xem INT,
                luot_nhan INT,
                ctr FLOAT,
                cpc FLOAT,
                cpm FLOAT,
                so_luong_mua_hang INT,
                conversion_rate FLOAT,
                cps FLOAT,
                videoview3s INT,
                videowatchesat25 INT,
                videowatchesat50 INT,
                videowatchesat75 INT,
                videowatchesat100 INT,
                ngay_bat_dau DATE,
                ngay_ket_thuc DATE,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (camp_type_id) REFERENCES campaign_type(camp_type_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (campstatus_id) REFERENCES campaign_status(campstatus_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (source_id) REFERENCES data_source(source_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO campaign (
                ten_chien_dich, camp_type_id, campstatus_id, 
                source_id, ngan_sach_ngay, tong_chi_phi, 
                luot_xem, luot_nhan, ctr, cpc, cpm, 
                so_luong_mua_hang, conversion_rate, cps,
                videoview3s, videowatchesat25, videowatchesat50,
                videowatchesat75, videowatchesat100,
                ngay_bat_dau, ngay_ket_thuc, active
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING camp_id
            ''', (
                self.ten_chien_dich, self.camp_type_id, self.campstatus_id,
                self.source_id, self.ngan_sach_ngay, self.tong_chi_phi,
                self.luot_xem, self.luot_nhan, self.ctr, self.cpc,
                self.cpm, self.so_luong_mua_hang, self.conversion_rate,
                self.cps, self.videoview3s, self.videowatchesat25,
                self.videowatchesat50, self.videowatchesat75,
                self.videowatchesat100, self.ngay_bat_dau,
                self.ngay_ket_thuc, self.active
            ))
            camp_id = cursor.fetchone()[0]
            conn.commit()
            return camp_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT 
                    camp_id, 
                    ten_chien_dich, 
                    campaign_type.ten_loai_chien_dich AS ten_loai_quang_cao,
                    ngan_sach_ngay, 
                    tong_chi_phi, 
                    luot_xem, 
                    luot_nhan, 
                    ctr, 
                    cpc, 
                    cpm, 
                    so_luong_mua_hang, 
                    conversion_rate, 
                    cps, 
                    videoview3s, 
                    videowatchesat25, 
                    videowatchesat50, 
                    videowatchesat75, 
                    videowatchesat100, 
                    ngay_bat_dau, 
                    ngay_ket_thuc, 
                    campaign.created_at, 
                    campaign.updated_at, 
                    campaign.active 
                FROM campaign 
                LEFT JOIN campaign_type ON campaign.camp_type_id = campaign_type.camp_type_id 
                ORDER BY campaign.created_at DESC
                ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(camp_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT c.*, ct.ten_loai_chien_dich as ten_loai_quang_cao
            FROM campaign c
            LEFT JOIN campaign_type ct ON c.camp_type_id = ct.camp_type_id
            WHERE c.camp_id = %s
            ''', (camp_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_name(ten_chien_dich):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM campaign WHERE ten_chien_dich ILIKE %s', (f'%{ten_chien_dich}%',))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def update(camp_id, data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build update query dynamically
            update_fields = []
            params = []
            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)
            
            if update_fields:
                params.append(camp_id)
                query = f'''
                UPDATE campaign 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE camp_id = %s
                '''
                cursor.execute(query, params)
                conn.commit()
                return True
            return False

    @staticmethod
    def delete(camp_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE campaign 
            SET active = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE camp_id = %s
            ''', (camp_id,))
            conn.commit()
            return True

    @staticmethod
    def get_dashboard_stats():
        """Get campaign statistics for dashboard"""
        return {
            'active_campaigns': 300,
            'remaining_budget': 80000000,
            'used_budget': 20000000,
            'views': 600000,
            'clicks': 10000000,
            'ctr': 2.3,
            'total_cost': 100000000000
        }
