from flask import Blueprint, request, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename
from models.product import Product

class ProductImportController(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file provided'}, 400
            
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No file selected'}, 400
            
        if not file.filename.endswith('.xlsx'):
            return {'error': 'Invalid file format. Please upload an Excel file'}, 400
            
        try:
            products = Product.import_from_excel(file.read())
            return {
                'message': f'Successfully imported {len(products)} products',
                'products': [vars(p) for p in products]
            }, 201
        except Exception as e:
            return {'error': str(e)}, 500 