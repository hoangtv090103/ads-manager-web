from configs.db import get_db_connection


class ProductGroup:
    def __init__(self, group_id=None, ten_nhom="", mo_ta="", parent_id=None):
        self.group_id = group_id
        self.ten_nhom = ten_nhom
        self.mo_ta = mo_ta
        self.parent_id = parent_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_group (
                group_id SERIAL PRIMARY KEY,
                ten_nhom VARCHAR(100) NOT NULL,
                mo_ta TEXT,
                parent_id INTEGER,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (parent_id) REFERENCES product_group(group_id)
                    ON DELETE SET NULL
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO product_group (ten_nhom, mo_ta, parent_id)
            VALUES (?, ?, ?)
            RETURNING group_id
            ''', (self.ten_nhom, self.mo_ta, self.parent_id))
            self.group_id = cursor.fetchone()[0]
            conn.commit()
            return self.group_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM product_group WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM product_group WHERE group_id = ? AND active = true', (group_id,))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE product_group 
            SET ten_nhom = ?, mo_ta = ?, parent_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE group_id = ?
            ''', (self.ten_nhom, self.mo_ta, self.parent_id, self.group_id))
            conn.commit()

    @staticmethod
    def delete(group_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE product_group SET active = false WHERE group_id = ?', (group_id,))
            conn.commit()
