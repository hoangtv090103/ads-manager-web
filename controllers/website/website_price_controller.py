from flask import request
from flask_restful import Resource, marshal_with, fields

from models.website.website_price import WebsitePrice

website_price_fields = {
    'price_id': fields.Integer,
    'pub_id': fields.Integer,
    'website_id': fields.Integer,
    'pricetype_id': fields.Integer,
    'pricestatus_id': fields.Integer,
    'thoi_gian_ap_dung': fields.DateTime,
    'zone_id': fields.Integer,
    'zonestatus_id': fields.Integer,
    'adstype_id': fields.Integer,
    'format_id': fields.Integer,
    'gia_mua': fields.Float,
    'gia_ban': fields.Float
}

class WebsitePriceController(Resource):
    @marshal_with(website_price_fields)
    def get(self, price_id=None):
        try:
            if price_id:
                return WebsitePrice.get_by_id(price_id)
            return WebsitePrice.get_all()
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            website_price = WebsitePrice(**data)
            website_price.create()
            return {'message': 'Website price created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

    def put(self, price_id):
        try:
            data = request.get_json()
            website_price = WebsitePrice(**data)
            website_price.price_id = price_id
            website_price.update()
            return {'message': 'Website price updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400 