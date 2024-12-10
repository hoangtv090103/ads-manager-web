from configs.db import get_db_connection


class DataSource:
    def __init__(self, source_id=None, ten_nguon_du_lieu="", source_status_id=None,
                 user_id=None, created_at=None, updated_at=None, active=True):
        self.source_id = source_id
        self.ten_nguon_du_lieu = ten_nguon_du_lieu
        self.source_status_id = source_status_id
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_source (
                source_id SERIAL PRIMARY KEY,
                ten_nguon_du_lieu TEXT NOT NULL,
                source_status_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (source_status_id) REFERENCES source_status(source_status_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO data_source (
                ten_nguon_du_lieu, source_status_id, user_id, active
            ) VALUES (%s, %s, %s, %s)
            ''', (self.ten_nguon_du_lieu, self.source_status_id, self.user_id, self.active))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ds.source_id, ds.ten_nguon_du_lieu, ds.source_status_id,
                       ds.user_id, ds.created_at, ds.updated_at,
                       u.username, ss.status_name
                FROM data_source ds
                LEFT JOIN users u ON ds.user_id = u.user_id
                LEFT JOIN source_status ss ON ds.source_status_id = ss.source_status_id
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row))
                    for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE data_source 
            SET ten_nguon_du_lieu = %s,
                source_status_id = %s,
                user_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE source_id = %s
            ''', (self.ten_nguon_du_lieu, self.source_status_id,
                  self.user_id, self.source_id))
            conn.commit()

    @staticmethod
    def get_by_id(source_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ds.*, u.username, ss.status_name
                FROM data_source ds
                LEFT JOIN users u ON ds.user_id = u.user_id
                LEFT JOIN source_status ss ON ds.source_status_id = ss.source_status_id
                WHERE ds.source_id = %s
            ''', (source_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))
