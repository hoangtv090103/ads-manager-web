from configs.db import get_db_connection

class SourceStatus:
    def __init__(self, source_status_id=None, ten_trang_thai="",
                 created_at=None, updated_at=None, active=True):
        self.source_status_id = source_status_id
        self.ten_trang_thai = ten_trang_thai
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS source_status (
                source_status_id SERIAL PRIMARY KEY,
                ten_trang_thai VARCHAR(50) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO source_status (ten_trang_thai)
            VALUES (%s)
            RETURNING source_status_id
            ''', (self.ten_trang_thai,))
            self.source_status_id = cursor.fetchone()[0]
            conn.commit()
            return self.source_status_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT source_status_id, ten_trang_thai, created_at, updated_at, active
                FROM source_status 
                WHERE active = TRUE
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(source_status_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT source_status_id, ten_trang_thai, created_at, updated_at, active
                FROM source_status 
                WHERE source_status_id = %s AND active = TRUE
            ''', (source_status_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def update(source_status_id, data={}):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            update_fields = []
            params = []
            
            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)
                    
            if update_fields:
                query = f'''
                UPDATE source_status 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE source_status_id = %s AND active = TRUE
                '''
                params.append(source_status_id)
                
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(source_status_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE source_status SET active = FALSE 
            WHERE source_status_id = %s
            ''', (source_status_id,))
            conn.commit() 