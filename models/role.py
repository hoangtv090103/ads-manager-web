from configs.db import get_db_connection


class Role:
    ADMIN = 1
    USER = 2

    def __init__(self, role_id=None, name="", description=""):
        self.role_id = role_id
        self.name = name
        self.description = description

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS role (
                role_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')

            # Insert default roles if they don't exist
            cursor.execute('SELECT COUNT(*) FROM role')
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    '''
                    INSERT INTO role (name, description) VALUES (%s, %s)
                    ''',
                    [
                        ('Admin', 'Quản trị viên hệ thống'),
                        ('User', 'Người dùng hệ thống')
                    ]
                )
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role_id, name, description, created_at, updated_at, active 
                FROM role 
                WHERE active = true
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_name(name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role_id FROM role WHERE name ILIKE %s AND active = true
            ''', (name,))
            row = cursor.fetchone()
            if not row:
                return None
            return row[0]

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO role (name, description) 
            VALUES (%s, %s)
            ''', (self.name, self.description))
            conn.commit()

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE role
            SET name = %s, description = %s
            WHERE role_id = %s
            ''', (self.name, self.description, self.role_id))
            conn.commit()

    @staticmethod
    def delete_by_id(role_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE role SET active = 0 WHERE role_id = %s', (role_id,))
            conn.commit()

    @staticmethod
    def get_by_id(role_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role_id, name, description, created_at, updated_at, active 
                FROM role 
                WHERE role_id = %s
            ''', (role_id,))
            return cursor.fetchone()

