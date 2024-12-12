from flask import jsonify, request
from flask_restful import Resource
from models.auth import Auth
from models.user import User
from models.publisher import Publisher
from models.customer import Customer
from models.role import Role
from configs.db import get_db_connection
from controllers.base_controller import BaseController


class AccountController(BaseController):
    def post(self):
        conn = None
        try:
            data = request.get_json()
            # Extract base user data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            fullname = data.get('fullname')
            phone = data.get('phone')
            is_admin = data.get('is_admin', False)
            status = data.get('status', True)
            user_type = data.get('user_type')  # 'publisher' or 'customer'

            # Validate required fields
            if not all([username, email, password, fullname, phone]):
                return jsonify({
                    'status': 'error',
                    'message': 'Missing required fields'
                }), 400

            # Non-admin users must have a user type
            if not is_admin and not user_type:
                return jsonify({
                    'status': 'error',
                    'message': 'User type is required for non-admin users'
                }), 400

            # Get appropriate role
            role_id = Role.get_by_name('Admin' if is_admin else 'User')
            if not role_id:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid role configuration'
                }), 400

            # Start transaction
            conn = get_db_connection()
            conn.autocommit = False

            # Create user account
            cursor = conn.cursor()

            # Check if email exists
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            if cursor.fetchone()[0] > 0:
                conn.rollback()
                return jsonify({
                    'status': 'error',
                    'message': 'User with this email already exists'
                }), 400

            # Insert user
            hashed_password = Auth.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password, role_id)
                VALUES (%s, %s, %s, %s) RETURNING user_id
            """, (username, email, hashed_password, role_id))
            user_id = cursor.fetchone()[0]

            # For non-admin users, create associated profile
            if not is_admin:
                if user_type == 'publisher':
                    pub_status_id = PublisherStatus.get_by_name(
                        'Hoạt động' if status else 'Tạm khóa')
                    cursor.execute("""
                        INSERT INTO publisher (ten_publisher, email, so_dien_thoai, pub_status_id, user_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (fullname, email, phone, pub_status_id, user_id))
                elif user_type == 'customer':
                    cursor.execute("""
                        INSERT INTO customer (ho_va_ten, email_doanh_nghiep, so_dien_thoai, user_id, active)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (fullname, email, phone, user_id, True))

            # If everything is successful, commit the transaction
            conn.commit()

            return jsonify({
                'status': 'success',
                'message': 'Account created successfully',
                'user_id': user_id,
                'role': 'Admin' if is_admin else 'User',
                'type': user_type if not is_admin else None
            })

        except Exception as e:
            # If any error occurs, rollback the transaction
            if conn:
                conn.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
        finally:
            if conn:
                conn.close()

    def get(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # Get all users with their roles
                cursor.execute("""
                    SELECT 
                        u.user_id,
                        u.username,
                        u.email,
                        u.active as user_active,
                        u.created_at,
                        r.name,
                        -- Publisher info
                        p.publisher_id,
                        p.ten_publisher,
                        p.so_dien_thoai as publisher_phone,
                        p.pub_status_id,
                        p.active as publisher_active,
                        -- Customer info
                        c.customer_id,
                        c.ho_va_ten,
                        c.so_dien_thoai as customer_phone,
                        c.email_doanh_nghiep,
                        c.active as customer_active
                    FROM users u
                    LEFT JOIN role r ON u.role_id = r.role_id
                    LEFT JOIN publisher p ON u.user_id = p.user_id
                    LEFT JOIN customer c ON u.user_id = c.user_id
                    ORDER BY u.created_at DESC
                """)

                users = []
                for row in cursor.fetchall():
                    user_type = 'Khách hàng' if row[12] else (
                        'Publisher' if row[7] else 'Admin')

                    users.append({
                        'user_id': row[0],
                        'username': row[1],
                        'email': row[2],
                        'active': row[3],
                        'created_at': row[4].strftime('%d/%m/%Y') if row[4] else None,
                        'role': row[5],
                        # ten_publisher or ho_va_ten or username
                        'full_name': row[7] or row[12] or row[1],
                        'user_type': user_type,
                        # Use user active status for all types
                        'status': row[3]
                    })

                return jsonify({
                    'status': 'success',
                    'data': users
                })

        except Exception as e:
            print("Error:", str(e))  # Add this for debugging
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def put(self, user_id):
        try:
            data = request.get_json()
            active = data.get('active')

            with get_db_connection() as conn:
                cursor = conn.cursor()

                # Start transaction
                conn.autocommit = False

                try:
                    # Update user status
                    cursor.execute("""
                        UPDATE users 
                        SET active = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = %s
                        RETURNING role_id
                    """, (active, user_id))

                    result = cursor.fetchone()
                    if not result:
                        conn.rollback()
                        return jsonify({
                            'status': 'error',
                            'message': 'User not found'
                        }), 404

                    # Get user type
                    cursor.execute("""
                        SELECT r.name 
                        FROM role r 
                        WHERE r.role_id = %s
                    """, (result[0],))

                    role = cursor.fetchone()[0]

                    # Update associated profile status
                    if role != 'Admin':
                        # Update publisher status if exists
                        cursor.execute("""
                            UPDATE publisher 
                            SET active = %s,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE user_id = %s
                        """, (active, user_id))

                        # Update customer status if exists
                        cursor.execute("""
                            UPDATE customer 
                            SET active = %s,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE user_id = %s
                        """, (active, user_id))

                    # Commit transaction
                    conn.commit()

                    return jsonify({
                        'status': 'success',
                        'message': 'User status updated successfully'
                    })

                except Exception as e:
                    conn.rollback()
                    raise e

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
