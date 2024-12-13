import bcrypt
from flask import request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from models.auth import Auth
from models.role import Role
from models.user import User
from flask_cors import cross_origin
from controllers.base_controller import BaseController


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

                response = make_response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'token': token,
                        'user': {
                            'id': user['user_id'],
                            'role': Role.get_by_id(user['role_id'])
                        }
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
