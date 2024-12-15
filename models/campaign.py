from configs.db import get_db_connection
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Campaign:
    def __init__(self, camp_id=None, ten_chien_dich="", camp_type_id=None,
                 customer_id=None, campstatus_id=None, source_id=None, ngan_sach_ngay=0,
                 tong_chi_phi=0, luot_xem=0, luot_nhan=0, ctr=0, cpc=0,
                 cpm=0, so_luong_mua_hang=0, conversion_rate=0, cps=0,
                 videoview3s=0, videowatchesat25=0, videowatchesat50=0,
                 videowatchesat75=0, videowatchesat100=0,
                 created_at=None, updated_at=None, active=True, ngay_bat_dau=None, ngay_ket_thuc=None):
        self.camp_id = camp_id
        self.ten_chien_dich = ten_chien_dich
        self.camp_type_id = camp_type_id  # 1: Display, 2: Native, 3: Video
        self.customer_id = customer_id
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
                customer_id INTEGER,
                camp_type_id INTEGER,
                campstatus_id INTEGER,
                source_id INTEGER,
                ten_chien_dich VARCHAR(100),
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
                ngay_bat_dau TIMESTAMPTZ,
                ngay_ket_thuc TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (customer_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (camp_type_id) REFERENCES campaign_type(camp_type_id) ON DELETE CASCADE,
                FOREIGN KEY (campstatus_id) REFERENCES campaign_status(campstatus_id) ON DELETE CASCADE,
                FOREIGN KEY (source_id) REFERENCES data_source(source_id) ON DELETE CASCADE
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
                ngay_bat_dau, ngay_ket_thuc, customer_id,
                created_at, updated_at, active
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE
            )
            RETURNING camp_id
            ''', (
                self.ten_chien_dich, self.camp_type_id, self.campstatus_id,
                self.source_id, self.ngan_sach_ngay, self.tong_chi_phi,
                self.ngay_bat_dau, self.ngay_ket_thuc, self.customer_id
            ))
            camp_id = cursor.fetchone()[0]
            conn.commit()
            return camp_id

    @staticmethod
    def get_all():
        logger.debug("Attempting to get all campaigns")
        try:
            with get_db_connection() as conn:
                logger.debug("Database connection established")
                cursor = conn.cursor()
                
                query = '''SELECT 
                    campaign.camp_id, 
                    campaign.ten_chien_dich, 
                    campaign_type.ten_loai_chien_dich AS ten_loai_quang_cao,
                    campaign.ngan_sach_ngay, 
                    campaign.tong_chi_phi, 
                    campaign.luot_xem, 
                    campaign.luot_nhan, 
                    campaign.ctr, 
                    campaign.cpc, 
                    campaign.cpm, 
                    campaign.so_luong_mua_hang, 
                    campaign.conversion_rate, 
                    campaign.cps, 
                    campaign.videoview3s, 
                    campaign.videowatchesat25, 
                    campaign.videowatchesat50, 
                    campaign.videowatchesat75, 
                    campaign.videowatchesat100,
                    campaign.ngay_bat_dau, 
                    campaign.ngay_ket_thuc,
                    campaign.created_at, 
                    campaign.updated_at, 
                    campaign_status.ten_trang_thai,
                    campaign.active,
                    customer.ho_va_ten
                FROM campaign 
                LEFT JOIN campaign_type ON campaign.camp_type_id = campaign_type.camp_type_id 
                LEFT JOIN campaign_status ON campaign.campstatus_id = campaign_status.campstatus_id
                LEFT JOIN customer ON campaign.customer_id = customer.customer_id
                ORDER BY campaign.created_at DESC'''
                
                logger.debug(f"Executing query: {query}")
                cursor.execute(query)
                
                rows = cursor.fetchall()
                logger.debug(f"Found {len(rows) if rows else 0} campaigns")
                
                if not rows:
                    logger.warning("No campaigns found in database")
                    return []
                    
                columns = [column[0] for column in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                logger.debug("Successfully converted rows to dictionaries")
                
                return result
                
        except Exception as e:
            logger.error(f"Error in get_all campaigns: {str(e)}", exc_info=True)
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def get_by_id(camp_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT c.*, ct.ten_loai_chien_dich as ten_loai_quang_cao, cs.ten_trang_thai
            FROM campaign c
            LEFT JOIN campaign_type ct ON c.camp_type_id = ct.camp_type_id
            LEFT JOIN campaign_status cs ON c.campstatus_id = cs.campstatus_id
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
            like_pattern = f'%{ten_chien_dich}%'
            cursor.execute(
                '''
                SELECT c.*, cs.ten_trang_thai
                FROM campaign c
                LEFT JOIN campaign_status cs ON c.campstatus_id = cs.campstatus_id
                WHERE c.ten_chien_dich ILIKE %s
                ''', (like_pattern,))
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
                SET {', '.join(update_fields)}
                WHERE camp_id = %s
                RETURNING camp_id
                '''

                cursor.execute(query, params)
                updated_row = cursor.fetchone()
                conn.commit()

                return updated_row is not None

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
