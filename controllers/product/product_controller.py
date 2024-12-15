from flask import request, jsonify
from flask_restful import Resource
from models.product import Product
from controllers.base_controller import BaseController


class ProductController(BaseController):
    def get(self, product_id=None):
        try:
            if product_id:
                product = Product.get_by_id(product_id)
                if not product:
                    return jsonify({
                        'message': 'Product not found',
                        'data': None
                    })
                
                return jsonify({
                    'message': 'Product retrieved successfully',
                    'data': product
                })
            else:
                products = Product.get_all()
                return jsonify({
                    'message': 'Products retrieved successfully',
                    'data': products
                })
        except Exception as e:
            return jsonify({
                'message': str(e)
            })

    def put(self, product_id):
        try:
            data = request.get_json()
            product = Product.get_by_id(product_id)
            if not product:
                return jsonify({
                    'message': 'Product not found',
                    'data': None
                })

            # Update product status
            Product.update_status(product_id, data.get('active', True))

            return jsonify({
                'message': 'Product updated successfully',
                'data': None
            })
        except Exception as e:
            return jsonify({
                'message': str(e)
            })

    def post(self):
        try:
            data = request.get_json()
            product = Product(**data)
            product.save()
            return {'message': 'Product created successfully'}
        except Exception as e:
            return {'message': str(e)}

    def delete(self, product_id):
        try:
            Product.delete_by_id(product_id)
            return {'message': 'Product deleted successfully'}
        except Exception as e:
            return {'message': str(e)}
