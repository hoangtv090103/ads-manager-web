from flask import request
from flask_restful import Resource, marshal_with, fields
from models.role import Role
from controllers.base_controller import BaseController
role_fields = {
    'role_id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}


class RoleController(BaseController):
    @marshal_with(role_fields)
    def get(self, role_id=None):
        try:
            if role_id:
                return Role.get_by_id(role_id)
            return Role.get_all()
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            role = Role(**data)
            role.save()
            return {'message': 'Role created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 400
