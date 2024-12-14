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
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return {'status': 'error', 'message': 'Email không được để trống'}, 400

            user = User.get_by_email(email)
            if not user:
                return {'status': 'error', 'message': 'Email không tồn tại trong hệ thống'}, 404

            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            expiry = datetime.utcnow() + timedelta(hours=24)

            # Save reset token to database
            Auth.save_reset_token(user['user_id'], reset_token, expiry)

            # Return token directly instead of sending email
            return {
                'status': 'success',
                'message': 'Xác thực email thành công',
                'data': {
                    'token': reset_token,
                    'email': email
                }
            }

        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500


class ResetPasswordController(BaseController):
    def post(self):
        try:
            data = request.get_json()
            token = data.get('token')
            new_password = data.get('password')

            if not token or not new_password:
                return {
                    'status': 'error',
                    'message': 'Token và mật khẩu mới không được để trống'
                }, 400

            # Verify token and get user_id
            user_id = Auth.verify_reset_token(token)
            if not user_id:
                return {
                    'status': 'error',
                    'message': 'Token không hợp lệ hoặc đã hết hạn'
                }, 400

            # Reset password
            if Auth.reset_password(user_id, new_password):
                return {
                    'status': 'success',
                    'message': 'Mật khẩu đã được đặt lại thành công'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Không thể đặt lại mật khẩu'
                }, 500

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500
