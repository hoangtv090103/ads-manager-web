from functools import wraps
from flask import request, jsonify
import jwt
import os
from datetime import datetime

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Lấy token từ header Authorization 
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token is missing!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Giải mã token
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
            
            # Kiểm tra token hết hạn
            if 'exp' in data and datetime.fromtimestamp(data['exp']) < datetime.utcnow():
                return jsonify({'message': 'Token has expired!'}), 401
                
            # Thêm thông tin user vào request
            request.user = {
                'user_id': data['user_id'],
                'role_id': data['role_id']
            }
            
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(*args, **kwargs)
    return decorated 