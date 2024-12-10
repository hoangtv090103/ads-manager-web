from flask import request
from flask_restful import Resource, fields, marshal_with

from models.product_group import ProductGroup

product_group_fields = {
    'group_id': fields.Integer,
    'ten_nhom': fields.String,
    'mo_ta': fields.String,
    'parent_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class ProductGroupController(Resource):
    @marshal_with(product_group_fields)
    def get(self, group_id=None):
        try:
            if group_id:
                return ProductGroup.get_by_id(group_id)
            return ProductGroup.get_all()
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            group = ProductGroup(**data)
            group.save()
            return {'message': 'Product group created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

    def put(self, group_id):
        try:
            data = request.get_json()
            group = ProductGroup(**data)
            group.productgroup_id = group_id
            group.update()
            return {'message': 'Product group updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, group_id):
        try:
            ProductGroup.delete(group_id)
            return {'message': 'Product group deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400 