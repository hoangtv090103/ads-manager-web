from configs.db import get_db_connection
import hashlib


class AuthController:
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
                if AuthController.verify_password(password, user['password']):
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
