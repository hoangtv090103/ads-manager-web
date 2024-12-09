from configs.db import get_db_connection

class Behaviour:
    def __init__(self, behav_id=None, ten_hanh_vi=""):
        self.behav_id = behav_id
        self.ten_hanh_vi = ten_hanh_vi

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS behaviour (
                behav_id SERIAL PRIMARY KEY,
                ten_hanh_vi TEXT NOT NULL,
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
            INSERT INTO behaviour (ten_hanh_vi)
            VALUES (%s)
            RETURNING behav_id
            ''', (self.ten_hanh_vi,))
            self.behav_id = cursor.fetchone()[0]
            conn.commit()
            return self.behav_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT behav_id, ten_hanh_vi, created_at, updated_at, active
                FROM behaviour 
                WHERE active = TRUE
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(behav_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT behav_id, ten_hanh_vi, created_at, updated_at, active
                FROM behaviour 
                WHERE behav_id = %s AND active = TRUE
            ''', (behav_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def update(behav_id, data={}):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            update_fields = []
            params = []
            
            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)
                    
            if update_fields:
                query = f'''
                UPDATE behaviour 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE behav_id = %s AND active = TRUE
                '''
                params.append(behav_id)
                
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(behav_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE behaviour SET active = FALSE 
            WHERE behav_id = %s
            ''', (behav_id,))
            conn.commit() 