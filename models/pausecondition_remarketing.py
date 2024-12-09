from configs.db import get_db_connection
class PauseConditionRemarketing:
    def __init__(self, condition_id=None, ten_loai_nham_chon="", nham_chon_tu_dong=""):
        self.condition_id = condition_id
        self.ten_loai_nham_chon = ten_loai_nham_chon
        self.nham_chon_tu_dong = nham_chon_tu_dong

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS pause_condition_remarketing (
                condition_id SERIAL PRIMARY KEY,
                ten_loai_nham_chon VARCHAR(50),
                nham_chon_tu_dong VARCHAR(50),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()