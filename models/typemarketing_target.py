from configs.db import get_db_connection

class TypeRemarketingTarget:
    def __init__(self, typeremarketing_id=None, ten_loai_nham_chon=""):
        self.typeremarketing_id = typeremarketing_id
        self.ten_loai_nham_chon = ten_loai_nham_chon

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS type_remarketing_target (
                typeremarketing_id SERIAL PRIMARY KEY,
                ten_loai_nham_chon VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO type_remarketing_target (ten_loai_nham_chon)
            VALUES (?)
            ''', (self.ten_loai_nham_chon,))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT typeremarketing_id, ten_loai_nham_chon, created_at, updated_at, active 
            FROM type_remarketing_target WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE type_remarketing_target
            SET ten_loai_nham_chon = ?, updated_at = CURRENT_TIMESTAMP
            WHERE typeremarketing_id = ?
            ''', (self.ten_loai_nham_chon, self.typeremarketing_id))
            conn.commit()

    @staticmethod
    def delete_by_id(typeremarketing_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE type_remarketing_target SET active = 0 WHERE typeremarketing_id = ?
            ''', (typeremarketing_id,))
            conn.commit()
