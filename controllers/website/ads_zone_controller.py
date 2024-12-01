from flask import request
from flask_restful import Resource, marshal_with, fields

from models.website.ads_zone import AdsZone

ads_zone_fields = {
    'zone_id': fields.Integer,
    'website_id': fields.Integer,
    'ten_vung_quang_cao': fields.String,
    'size_id': fields.Integer,
    'adstype_id': fields.Integer,
    'ma_dinh_dang': fields.String,
    'qc_du_phong': fields.String,
    'ma_nhung_vung_quang_cao': fields.String
}


class AdsZoneController(Resource):
    @marshal_with(ads_zone_fields)
    def get(self, zone_id=None):
        try:
            if zone_id:
                return AdsZone.get_by_id(zone_id)
            return AdsZone.get_all()
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            ads_zone = AdsZone(**data)
            ads_zone.save()
            return {'message': 'Ads zone created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

    def put(self, zone_id):
        try:
            data = request.get_json()
            ads_zone = AdsZone(**data)
            ads_zone.zone_id = zone_id
            ads_zone.update()
            return {'message': 'Ads zone updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400
