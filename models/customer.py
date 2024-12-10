from configs.db import get_db_connection


class Customer:
    def __init__(self, customer_id=None, ho_va_ten="", ngay_sinh=None, gioi_tinh=None,
                 ten_doanh_nghiep="", dia_chi_doanh_nghiep="", country_id=None,
                 city_id=None, district_id=None, website_doanh_nghiep="",
                 so_dien_thoai="", email_doanh_nghiep="", ma_remarketing="",
                 created_at=None, updated_at=None, active=True):
        self.customer_id = customer_id
        self.ho_va_ten = ho_va_ten
        self.ngay_sinh = ngay_sinh
        self.gioi_tinh = gioi_tinh
        self.ten_doanh_nghiep = ten_doanh_nghiep
        self.dia_chi_doanh_nghiep = dia_chi_doanh_nghiep
        self.country_id = country_id
        self.city_id = city_id
        self.district_id = district_id
        self.website_doanh_nghiep = website_doanh_nghiep
        self.so_dien_thoai = so_dien_thoai
        self.email_doanh_nghiep = email_doanh_nghiep
        self.ma_remarketing = ma_remarketing
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer (
                customer_id SERIAL PRIMARY KEY,
                ho_va_ten VARCHAR(100),
                ngay_sinh DATE,
                gioi_tinh INTEGER,
                ten_doanh_nghiep VARCHAR(200),
                dia_chi_doanh_nghiep TEXT,
                country_id INTEGER,
                city_id INTEGER,
                district_id INTEGER,
                website_doanh_nghiep VARCHAR(255),
                so_dien_thoai VARCHAR(20),
                email_doanh_nghiep VARCHAR(100),
                ma_remarketing VARCHAR(100),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (country_id) REFERENCES country(country_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (city_id) REFERENCES city(city_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (district_id) REFERENCES district(district_id)
                    ON DELETE SET NULL
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Customer (
                customer_id, ho_va_ten, ngay_sinh, gioi_tinh, ten_doanh_nghiep,
                dia_chi_doanh_nghiep, country_id, city_id, district_id,
                website_doanh_nghiep, so_dien_thoai, email_doanh_nghiep,
                ma_remarketing
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.customer_id, self.ho_va_ten, self.ngay_sinh, self.gioi_tinh,
                self.ten_doanh_nghiep, self.dia_chi_doanh_nghiep, self.country_id,
                self.city_id, self.district_id, self.website_doanh_nghiep,
                self.so_dien_thoai, self.email_doanh_nghiep, self.ma_remarketing,
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM Customer WHERE active = true')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_email(email):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM Customer WHERE email_doanh_nghiep = ? AND active = true',
                (email,))
            row = cursor.fetchone()
            return dict(zip([column[0] for column in cursor.description], row)) if row else None

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE Customer
            SET ho_va_ten = ?, ngay_sinh = ?, gioi_tinh = ?, 
                ten_doanh_nghiep = ?, dia_chi_doanh_nghiep = ?, 
                country_id = ?, city_id = ?, district_id = ?, 
                website_doanh_nghiep = ?, so_dien_thoai = ?, 
                email_doanh_nghiep = ?, ma_remarketing = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE customer_id = ?
            ''', (
                self.ho_va_ten, self.ngay_sinh, self.gioi_tinh,
                self.ten_doanh_nghiep, self.dia_chi_doanh_nghiep,
                self.country_id, self.city_id, self.district_id,
                self.website_doanh_nghiep, self.so_dien_thoai,
                self.email_doanh_nghiep, self.ma_remarketing,
                self.customer_id
            ))
            conn.commit()

    @staticmethod
    def delete_by_id(customer_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE Customer SET active = 0 WHERE customer_id = ?', (customer_id,))
            conn.commit()
