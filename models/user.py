from configs.db import get_db_connection


class User:
    def __init__(self, user_id=None, username="", email="", password="",
                 role_id=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (role_id) REFERENCES role(role_id)
            )
            """)
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, email, role_id, created_at, updated_at, active 
                FROM users
            """)
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, email, role_id, created_at, updated_at, active FROM users WHERE user_id = %s
            """, (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_username(username):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, password, email, role_id, created_at, updated_at, active FROM users WHERE username = %s
            """, (username,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def create(username, email, password, role_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id FROM users WHERE email = ?
            """, (email,))
            if cursor.fetchone():
                raise Exception("User with this email already exists.")
            else:
                hashed_password = Auth.hash_password(password)
                cursor.execute("""
                    INSERT INTO users (username, email, password, role_id)
                    VALUES (?, ?, ?, ?)
                """, (username, email, hashed_password, role_id))
                conn.commit()
