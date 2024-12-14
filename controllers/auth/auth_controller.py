import bcrypt
from flask import request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from models.auth import Auth
from models.customer import Customer
from models.publisher import Publisher
from models.role import Role
from models.user import User
from flask_cors import cross_origin
from controllers.base_controller import BaseController
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class LoginController(BaseController):
    @cross_origin(supports_credentials=True)
    def post(self):
        try:
            data = request.get_json()
            user = User.get_by_username(data['username'])
            if not user:
                user = User.get_by_email(data['username'])

            if not user:
                return {'status': 'error', 'message': 'Invalid credentials'}, 401

            if user and Auth.verify_password(data.get('password'), user.get('password')) or user.get('password') == data.get('password'):
                token = jwt.encode({
                    'user_id': user['user_id'],
                    'role_id': user['role_id'],
                    'exp': datetime.utcnow() + timedelta(days=1)
                }, os.getenv('JWT_SECRET_KEY') or 'your-secret-key')

                ho_va_ten = ''
                publisher = Publisher.get_by_user_id(user['user_id'])
                customer = Customer.get_by_user_id(user['user_id'])
                if publisher:
                    ho_va_ten = publisher['ten_publisher']
                if customer:
                    ho_va_ten = customer['ho_va_ten']

                response = make_response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'token': token,
                        'user': {
                            'id': user['user_id'],
                            'username': user['username'],
                            'ho_va_ten': ho_va_ten,
                            'email': user['email'],
                            'role': Role.get_by_id(user['role_id'])
                        },
                        'customer': customer,
                        'publisher': publisher
                    }
                })
                return response

            return {'status': 'error', 'message': 'Invalid credentials'}, 401
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500


class RegisterController(BaseController):
    def post(self):
        try:
            data = request.get_json()

            # Hash password
            data['password'] = generate_password_hash(data['password'])

            user = User(**data)
            user.create()

            return {'message': 'User registered successfully'}
        except Exception as e:
            return {'message': str(e)}


class ForgotPasswordController(BaseController):
    @cross_origin(supports_credentials=True)
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return {'status': 'error', 'message': 'Email is required'}, 400

            user = User.get_by_email(email)
            if not user:
                return {'status': 'error', 'message': 'Email không tồn tại trong hệ thống'}, 404

            # Generate reset token
            token = jwt.encode({
                'user_id': user['user_id'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, os.getenv('JWT_SECRET_KEY') or 'your-secret-key')
            expiry = datetime.utcnow() + timedelta(hours=24)

            # Save token to database
            Auth.save_reset_token(user['user_id'], token, expiry)

            # Send reset email
            reset_link = f"http://localhost:5500/frontend/reset-password.html?token={token}&email={email}"
            print(reset_link)
            self.send_reset_email(email, reset_link)

            return {'status': 'success', 'message': 'Email đặt lại mật khẩu đã được gửi'}, 200

        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    def send_reset_email(self, email, reset_link):
        try:
            sender_email = os.getenv('EMAIL_USER')
            sender_password = os.getenv('EMAIL_PASSWORD')

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = "Đặt lại mật khẩu - Ads Manager"

            body = f"""
            <html>
              <body>
                <h2>Đặt lại mật khẩu</h2>
                <p>Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của mình.</p>
                <p>Vui lòng click vào link bên dưới để đặt lại mật khẩu:</p>
                <p><a href="{reset_link}">Đặt lại mật khẩu</a></p>
                <p>Link này sẽ hết hạn sau 24 giờ.</p>
                <p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
              </body>
            </html>
            """

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise Exception("Failed to send reset email")


class ResetPasswordController(BaseController):
    @cross_origin(supports_credentials=True)
    def post(self):
        try:
            data = request.get_json()
            token = data.get('token')
            email = data.get('email')
            new_password = data.get('new_password')

            if not all([token, email, new_password]):
                return {'status': 'error', 'message': 'Missing required fields'}, 400

            user = User.get_by_email(email)
            if not user:
                return {'status': 'error', 'message': 'Invalid email'}, 404

            # Verify token
            if not Auth.verify_reset_token(user['user_id'], token):
                return {'status': 'error', 'message': 'Invalid or expired token'}, 400

            # Update password
            hashed_password = Auth.hash_password(new_password)
            User.update_password(user['user_id'], hashed_password)

            # Mark token as used
            Auth.mark_token_as_used(token)

            return {'status': 'success', 'message': 'Password reset successfully'}, 200

        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
