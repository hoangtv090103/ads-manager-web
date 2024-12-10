from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with

from models.product import Product

product_fields = {
    'product_id': fields.Integer,
    'ten_san_pham': fields.String,
    'mo_ta_san_pham': fields.String,
    'lien_ket_san_pham': fields.String,
    'hinh_anh_san_pham': fields.Raw,
    'product_status_id': fields.Integer,
    'tinh_trang_san_pham': fields.String,
    'gia': fields.Float,
    'gia_khuyen_mai': fields.Float,
    'loai_san_pham': fields.String,
    'customer_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class ProductController(Resource):
    @marshal_with(product_fields)
    def get(self, product_id=None):
        try:
            if product_id:
                return Product.get_by_id(product_id)
            return Product.get_all()
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            product = Product(**data)
            product.save()
            return {'message': 'Product created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

    def put(self, product_id):
        try:
            data = request.get_json()
            product = Product(**data)
            product.product_id = product_id
            product.update()
            return {'message': 'Product updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, product_id):
        try:
            Product.delete_by_id(product_id)
            return {'message': 'Product deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400 