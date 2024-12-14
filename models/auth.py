import hashlib
from datetime import datetime
from configs.db import get_db_connection


class Auth:
    @staticmethod
    def login(username, password):
        """Authenticate user login"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Check if user exists and is active
            cursor.execute("""
                SELECT u.user_id, u.username, u.email, u.role_id, u.password, r.name as role_name
                FROM users u
                LEFT JOIN role r ON u.role_id = r.role_id
                WHERE u.username = %s
                AND u.active = true
            """, (username,))

            user = cursor.fetchone()
            if user:
                user = dict(
                    zip([column[0] for column in cursor.description], user)) if user else None

                # Check if password is correct
                if Auth.verify_password(password, user['password']):
                    return user
            return None

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password against hashed password"""

        if password == hashed_password \
                or hashlib.sha256(password.encode()).hexdigest() == hashed_password \
                or password == hashlib.sha256(hashed_password.encode()).hexdigest():
            return True
        return False

    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def save_reset_token(user_id, token, expiry):
        """Save password reset token to database"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO password_reset_tokens (user_id, token, expiry)
                VALUES (%s, %s, %s)
            """, (user_id, token, expiry))
            conn.commit()

    @staticmethod
    def verify_reset_token(user_id, token):
        """Verify if reset token is valid and not expired"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM password_reset_tokens
                WHERE user_id = %s AND token = %s AND expiry > %s AND used = false
                ORDER BY created_at DESC LIMIT 1
            """, (user_id, token, datetime.utcnow()))
            
            return cursor.fetchone() is not None

    @staticmethod
    def mark_token_as_used(token):
        """Mark reset token as used"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE password_reset_tokens
                SET used = true
                WHERE token = %s
            """, (token,))
            conn.commit()
