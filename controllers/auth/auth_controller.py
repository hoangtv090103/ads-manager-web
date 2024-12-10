from flask import request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from models.user import User
from flask_cors import cross_origin


class LoginController(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        try:
            data = request.get_json()
            user = User.get_by_username(data['username'])

            if user and check_password_hash(user.get('password'), data.get('password')) or user.get('password') == data.get('password'):
                token = jwt.encode({
                    'user_id': user['user_id'],
                    'role_id': user['role_id'],
                    'exp': datetime.utcnow() + timedelta(days=1)
                }, os.getenv('JWT_SECRET_KEY') or 'your-secret-key')

                response = make_response({'token': token})
                return response

            return {'message': 'Invalid credentials'}, 401
        except Exception as e:
            return {'message': str(e)}, 500


class RegisterController(Resource):
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
