from configs.db import get_db_connection
class Product:
    def __init__(self, product_id=None, ten_san_pham="", mo_ta_san_pham="",
                 lien_ket_san_pham="", hinh_anh_san_pham="", product_status_id=None,
                 tinh_trang_san_pham="", gia=0, gia_khuyen_mai=0, loai_san_pham="",
                 source_id=None, created_at=None, updated_at=None, active=True):
        self.product_id = product_id
        self.ten_san_pham = ten_san_pham
        self.mo_ta_san_pham = mo_ta_san_pham
        self.lien_ket_san_pham = lien_ket_san_pham
        self.hinh_anh_san_pham = hinh_anh_san_pham
        self.product_status_id = product_status_id
        self.tinh_trang_san_pham = tinh_trang_san_pham
        self.gia = gia
        self.gia_khuyen_mai = gia_khuyen_mai
        self.loai_san_pham = loai_san_pham
        self.source_id = source_id
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
                ten_san_pham VARCHAR(200) NOT NULL,
                mo_ta_san_pham TEXT,
                lien_ket_san_pham VARCHAR(255),
                hinh_anh_san_pham VARCHAR(255),
                product_status_id INTEGER,
                tinh_trang_san_pham VARCHAR(100),
                gia DECIMAL(15,2),
                gia_khuyen_mai DECIMAL(15,2),
                loai_san_pham VARCHAR(100),
                source_id INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (product_status_id) REFERENCES product_status(product_status_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (source_id) REFERENCES data_source(source_id)
                    ON DELETE SET NULL
            )
            ''')
            conn.commit() 