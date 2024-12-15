from configs.db import get_db_connection

class ProductGroup:
    def __init__(self, productgroup_id=None, ten_nhom="", source_id=None, 
                 phan_loai_theo=None, products=None):
        self.productgroup_id = productgroup_id
        self.ten_nhom = ten_nhom
        self.source_id = source_id
        self.phan_loai_theo = phan_loai_theo
        self.products = products or []

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_group (
                productgroup_id SERIAL PRIMARY KEY,
                ten_nhom VARCHAR(100) NOT NULL,
                source_id INTEGER,
                phan_loai_theo VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (source_id) REFERENCES data_source(source_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # Bắt đầu transaction
                cursor.execute('BEGIN')
                
                # Insert product group
                cursor.execute('''
                INSERT INTO product_group (ten_nhom, source_id, phan_loai_theo)
                VALUES (%s, %s, %s)
                RETURNING productgroup_id
                ''', (self.ten_nhom, self.source_id, self.phan_loai_theo))
                
                self.productgroup_id = cursor.fetchone()[0]
                
                # Insert product mappings
                if self.products:
                    cursor.executemany('''
                    INSERT INTO product_group_mapping (product_id, productgroup_id)
                    VALUES (%s, %s)
                    ''', [(product_id, self.productgroup_id) for product_id in self.products])
                
                # Commit transaction
                cursor.execute('COMMIT')
                return self.productgroup_id
                
            except Exception as e:
                cursor.execute('ROLLBACK')
                raise e

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pg.*, ds.ten_nguon_du_lieu as nguon_du_lieu,
                       COUNT(pgm.product_id) as so_luong
                FROM product_group pg
                LEFT JOIN data_source ds ON pg.source_id = ds.source_id
                LEFT JOIN product_group_mapping pgm ON pg.productgroup_id = pgm.productgroup_id
                WHERE pg.active = true
                GROUP BY pg.productgroup_id, ds.ten_nguon_du_lieu
                ORDER BY pg.created_at DESC
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(productgroup_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pg.*, ds.ten_nguon_du_lieu,
                       array_agg(pgm.product_id) as product_ids
                FROM product_group pg
                LEFT JOIN data_source ds ON pg.source_id = ds.source_id
                LEFT JOIN product_group_mapping pgm ON pg.productgroup_id = pgm.productgroup_id
                WHERE pg.productgroup_id = %s AND pg.active = true
                GROUP BY pg.productgroup_id, ds.ten_nguon_du_lieu
            ''', (productgroup_id,))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('BEGIN')
                
                # Update product group
                cursor.execute('''
                UPDATE product_group 
                SET ten_nhom = %s, source_id = %s, phan_loai_theo = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE productgroup_id = %s
                ''', (self.ten_nhom, self.source_id, self.phan_loai_theo, self.productgroup_id))

                # Delete old mappings
                cursor.execute('''
                DELETE FROM product_group_mapping 
                WHERE productgroup_id = %s
                ''', (self.productgroup_id,))

                # Insert new mappings
                if self.products:
                    cursor.executemany('''
                    INSERT INTO product_group_mapping (product_id, productgroup_id)
                    VALUES (%s, %s)
                    ''', [(product_id, self.productgroup_id) for product_id in self.products])

                cursor.execute('COMMIT')
            except Exception as e:
                cursor.execute('ROLLBACK')
                raise e

    @staticmethod
    def delete(productgroup_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE product_group 
            SET active = false, updated_at = CURRENT_TIMESTAMP
            WHERE productgroup_id = %s
            ''', (productgroup_id,))
            conn.commit()
