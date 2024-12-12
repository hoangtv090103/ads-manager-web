from configs.db import get_db_connection
from openpyxl import load_workbook
import io


class Product:
    def __init__(self, product_id=None, ten_san_pham="", mo_ta_san_pham="",
                 lien_ket_san_pham="", hinh_anh_san_pham=None,
                 source_id=None, productstatus_id=None,
                 gia_san_pham=None, gia_khuyen_mai=None,
                 created_at=None, updated_at=None, active=True):
        self.product_id = product_id
        self.ten_san_pham = ten_san_pham
        self.mo_ta_san_pham = mo_ta_san_pham
        self.lien_ket_san_pham = lien_ket_san_pham
        self.hinh_anh_san_pham = hinh_anh_san_pham
        self.source_id = source_id
        self.productstatus_id = productstatus_id
        self.gia_san_pham = gia_san_pham
        self.gia_khuyen_mai = gia_khuyen_mai
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS product (
                    product_id SERIAL PRIMARY KEY,
                    ten_san_pham VARCHAR(255),
                    mo_ta_san_pham TEXT,
                    lien_ket_san_pham VARCHAR(255),
                    hinh_anh_san_pham BYTEA,
                    source_id INTEGER,
                    productstatus_id INTEGER,
                    gia_san_pham DECIMAL(15,2),
                    gia_khuyen_mai DECIMAL(15,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (source_id) REFERENCES data_source(source_id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (productstatus_id) REFERENCES product_status(productstatus_id)
                        ON DELETE CASCADE
                )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO product (
                ten_san_pham, mo_ta_san_pham, lien_ket_san_pham,
                hinh_anh_san_pham, source_id, productstatus_id, gia_san_pham, gia_khuyen_mai, active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                self.ten_san_pham, self.mo_ta_san_pham,
                self.lien_ket_san_pham, self.hinh_anh_san_pham,
                self.source_id, self.productstatus_id, self.active
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, 
                       ds.ten_nguon_du_lieu,
                       ps.status_name as product_status_name
                FROM product p
                LEFT JOIN data_source ds ON p.source_id = ds.source_id
                LEFT JOIN product_status ps ON p.productstatus_id = ps.productstatus_id
                WHERE p.active = true
                ORDER BY p.created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row))
                    for row in rows]

    @staticmethod
    def get_by_id(product_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, 
                       ds.ten_nguon_du_lieu,
                       ps.status_name as product_status_name
                FROM product p
                LEFT JOIN data_source ds ON p.source_id = ds.source_id
                LEFT JOIN product_status ps ON p.productstatus_id = ps.productstatus_id
                WHERE p.product_id = %s
            ''', (product_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE product
            SET ten_san_pham = %s,
                mo_ta_san_pham = %s,
                lien_ket_san_pham = %s,
                hinh_anh_san_pham = %s,
                source_id = %s,
                productstatus_id = %s,
                gia_san_pham = %s,
                gia_khuyen_mai = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE product_id = %s
            ''', (
                self.ten_san_pham, self.mo_ta_san_pham,
                self.lien_ket_san_pham, self.hinh_anh_san_pham,
                self.source_id, self.productstatus_id,
                self.gia_san_pham, self.gia_khuyen_mai,
                self.product_id
            ))
            conn.commit()

    @staticmethod
    def delete_by_id(product_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE product 
            SET active = false,
                updated_at = CURRENT_TIMESTAMP
            WHERE product_id = %s
            ''', (product_id,))
            conn.commit()

    @staticmethod
    def import_from_excel(file_content):
        wb = load_workbook(filename=io.BytesIO(file_content))
        ws = wb.active
        products = []

        for row in ws.iter_rows(min_row=2):  # Skip header row
            product = Product(
                ten_san_pham=row[0].value,
                mo_ta_san_pham=row[1].value,
                lien_ket_san_pham=row[2].value,
                source_id=row[3].value,
                productstatus_id=row[4].value,
                gia_san_pham=row[5].value,
                gia_khuyen_mai=row[6].value
            )
            products.append(product)
            product.save()

        return products
