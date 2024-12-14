from configs.db import get_db_connection


class TargetAudience:
    def __init__(self, ta_id=None, ten_nhom_doi_tuong="", trang_da_truy_cap="",
                 apply_all_product=False, HanhViID=None, LoaiTruHanhViID=None,
                 created_at=None, updated_at=None, active=True):
        self.ta_id = ta_id
        self.ten_nhom_doi_tuong = ten_nhom_doi_tuong
        self.trang_da_truy_cap = trang_da_truy_cap
        self.apply_all_product = apply_all_product
        self.HanhViID = HanhViID
        self.LoaiTruHanhViID = LoaiTruHanhViID
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_audience (
                ta_id SERIAL PRIMARY KEY,
                ten_nhom_doi_tuong VARCHAR(100),
                trang_da_truy_cap TEXT,
                HanhViID INTEGER,
                LoaiTruHanhViID INTEGER,
                apply_all_product BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (HanhViID) REFERENCES behaviour(behav_id),
                FOREIGN KEY (LoaiTruHanhViID) REFERENCES behaviour(behav_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO target_audience (
                ten_nhom_doi_tuong, trang_da_truy_cap,
                apply_all_product, HanhViID, LoaiTruHanhViID
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ta_id
            ''', (
                self.ten_nhom_doi_tuong,
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
            SELECT *
            FROM target_audience
            WHERE active = TRUE
            ORDER BY created_at DESC
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
            try:
                # Update main record
                cursor.execute('''
                UPDATE target_audience
                SET ten_nhom_doi_tuong = %s,
                    trang_da_truy_cap = %s,
                    apply_all_product = %s,
                    product_type = %s,
                    product_include = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE ta_id = %s
                ''', (
                    self.ten_nhom_doi_tuong,
                    self.trang_da_truy_cap,
                    self.apply_all_product,
                    self.product_info.get('type') if not self.apply_all_product else None,
                    self.product_info.get('include') if not self.apply_all_product else None,
                    self.ta_id
                ))

                # Delete existing behaviors
                cursor.execute('''
                DELETE FROM target_audience_behavior
                WHERE ta_id = %s
                ''', (self.ta_id,))

                # Insert new behaviors
                for behavior in self.behaviors:
                    cursor.execute('''
                    INSERT INTO target_audience_behavior (
                        ta_id, behavior_id, is_excluded
                    )
                    VALUES (%s, %s, %s)
                    ''', (
                        self.ta_id,
                        behavior['behavior_id'],
                        behavior['is_excluded']
                    ))

                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e

    @staticmethod
    def delete_by_id(ta_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                UPDATE target_audience 
                SET active = FALSE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE ta_id = %s
                ''', (ta_id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
