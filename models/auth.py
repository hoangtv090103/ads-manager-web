import hashlib
from configs.db import get_db_connection
from datetime import datetime


class Auth:
    
    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # Create password_reset_tokens table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS password_reset_tokens (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                        token VARCHAR(255) NOT NULL UNIQUE,
                        expiry TIMESTAMP NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    used BOOLEAN DEFAULT FALSE
                    );
                """)

                conn.commit()
            except Exception as e:
                print(f"Error creating password_reset_tokens table: {str(e)}")

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
        """Save password reset token"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # Delete any existing reset tokens for this user
                cursor.execute("""
                    DELETE FROM password_reset_tokens
                    WHERE user_id = %s
                """, (user_id,))

                # Insert new reset token
                cursor.execute("""
                    INSERT INTO password_reset_tokens (user_id, token, expiry)
                    VALUES (%s, %s, %s)
                """, (user_id, token, expiry))

                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"Error saving reset token: {str(e)}")
                return False

    @staticmethod
    def verify_reset_token(token):
        """Verify if reset token is valid and not expired"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT user_id, expiry
                    FROM password_reset_tokens
                    WHERE token = %s
                """, (token,))

                result = cursor.fetchone()
                if not result:
                    return None

                user_id, expiry = result
                if expiry < datetime.utcnow():
                    return None

                return user_id
            except Exception as e:
                print(f"Error verifying reset token: {str(e)}")
                return None

    @staticmethod
    def reset_password(user_id, new_password):
        """Reset user's password"""
        try:
            # Validate password
            if not Auth.validate_password(new_password):
                raise Exception(
                    "Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường và số")

            with get_db_connection() as conn:
                cursor = conn.cursor()
                try:
                    hashed_password = Auth.hash_password(new_password)
                    cursor.execute("""
                        UPDATE users
                        SET password = %s
                        WHERE user_id = %s
                    """, (hashed_password, user_id))

                    # Delete used reset token
                    cursor.execute("""
                        DELETE FROM password_reset_tokens
                        WHERE user_id = %s
                    """, (user_id,))

                    conn.commit()
                    return True
                except Exception as e:
                    conn.rollback()
                    print(f"Error resetting password: {str(e)}")
                    return False
        except Exception as e:
            print(f"Error in reset_password: {str(e)}")
            raise

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False

        has_upper = False
        has_lower = False
        has_digit = False

        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True

        return has_upper and has_lower and has_digit
