from flask import request, jsonify
from flask_restful import Resource, marshal_with, fields

from models.website import Website


class WebsiteController(Resource):
    def get(self, website_id=None):
        try:
            data = request.args
            if website_id:
                return Website.get_by_id(website_id)
            elif data.get('has_price'):
                websites = Website.get_all_has_price_list()
            else:
                websites = Website.get_all()
            return jsonify(websites)
        except Exception as e:
            return jsonify({'message': str(e)})

    def post(self):
        try:
            data = request.get_json()
            website = Website(**data)
            website.create()
            return jsonify({'message': 'Website created successfully'})
        except Exception as e:
            return jsonify({'message': str(e)})

    def put(self, website_id):
        try:
            data = request.get_json()
            website = Website(**data)
            website.website_id = website_id
            website.update()
            return jsonify({'message': 'Website updated successfully'})
        except Exception as e:
            return jsonify({'message': str(e)})

    def delete(self, website_id):
        try:
            Website.delete_by_id(website_id)
            return jsonify({'message': 'Website deleted successfully'})
        except Exception as e:
            return jsonify({'message': str(e)})
