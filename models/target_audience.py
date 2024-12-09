from configs.db import get_db_connection

class TargetAudience:
    def __init__(self, ta_id=None, ten_nhom_doi_tuong="", ta_status_id=None,
                 trang_da_truy_cap="", apply_all_product=False,
                 HanhViID=None, LoaiTruHanhViID=None, created_at=None,
                 updated_at=None, status=True):
        self.ta_id = ta_id
        self.ten_nhom_doi_tuong = ten_nhom_doi_tuong
        self.ta_status_id = ta_status_id
        self.trang_da_truy_cap = trang_da_truy_cap
        self.apply_all_product = apply_all_product
        self.HanhViID = HanhViID
        self.LoaiTruHanhViID = LoaiTruHanhViID
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_audience (
                ta_id SERIAL PRIMARY KEY,
                ten_nhom_doi_tuong VARCHAR(100),
                ta_status_id INTEGER NOT NULL,
                trang_da_truy_cap TEXT,
                apply_all_product BOOLEAN DEFAULT FALSE,
                HanhViID INTEGER,
                LoaiTruHanhViID INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (ta_status_id) REFERENCES target_audience_status(ta_status_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO target_audience (
                ten_nhom_doi_tuong, ta_status_id, trang_da_truy_cap,
                apply_all_product, HanhViID, LoaiTruHanhViID
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING ta_id
            ''', (
                self.ten_nhom_doi_tuong, self.ta_status_id,
                self.trang_da_truy_cap, self.apply_all_product,
                self.HanhViID, self.LoaiTruHanhViID
            ))
            self.ta_id = cursor.fetchone()[0]
            conn.commit()
            return self.ta_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT ta.*, tas.ten_trang_thai
            FROM target_audience ta
            LEFT JOIN target_audience_status tas ON ta.ta_status_id = tas.ta_status_id
            WHERE ta.active = TRUE
            ORDER BY ta.created_at DESC
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(ta_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM target_audience 
            WHERE ta_id = %s AND active = TRUE
            ''', (ta_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE target_audience
            SET ten_nhom_doi_tuong = %s, ta_status_id = %s,
                trang_da_truy_cap = %s, apply_all_product = %s,
                HanhViID = %s, LoaiTruHanhViID = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE ta_id = %s
            ''', (
                self.ten_nhom_doi_tuong, self.ta_status_id,
                self.trang_da_truy_cap, self.apply_all_product,
                self.HanhViID, self.LoaiTruHanhViID, self.ta_id
            ))
            conn.commit()

    @staticmethod
    def delete_by_id(ta_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE target_audience SET active = FALSE 
            WHERE ta_id = %s
            ''', (ta_id,))
            conn.commit()
