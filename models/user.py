from configs.db import get_db_connection
from models.auth import Auth


class User:
    def __init__(self, user_id=None, username="", ho_va_ten="", email="", password="",
                 role_id=None):
        self.user_id = user_id
        self.username = username
        self.ho_va_ten = ho_va_ten
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
                ho_va_ten TEXT NOT NULL,
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
    def get_by_email(email):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, password, email, role_id, created_at, updated_at, active FROM users WHERE email = %s
            """, (email,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def create(username, ho_va_ten, email, password, role_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM users WHERE email = %s
            """, (email,))
            if cursor.fetchone()[0] > 0:
                raise Exception("User with this email already exists.")
            else:
                hashed_password = Auth.hash_password(password)
                cursor.execute("""
                    INSERT INTO users (username, ho_va_ten, email, password, role_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING user_id
                """, (username, ho_va_ten, email, hashed_password, role_id))
                user_id = cursor.fetchone()[0]
                conn.commit()
                return user_id

    @staticmethod
    def update_password(user_id, new_password):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password = %s WHERE user_id = %s
            """, (new_password, user_id))
            conn.commit()
