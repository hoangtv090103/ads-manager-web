from configs.db import get_db_connection
class DataSource:
    def __init__(self, source_id=None, ten_nguon_du_lieu="", source_status_id=None,
                 user_id=None, created_at=None, updated_at=None):
        self.source_id = source_id
        self.ten_nguon_du_lieu = ten_nguon_du_lieu
        self.source_status_id = source_status_id
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_source (
                source_id SERIAL PRIMARY KEY,
                ten_nguon_du_lieu VARCHAR(100),
                source_status_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (source_status_id) REFERENCES source_status(source_status_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit() 