from flask import request, jsonify
from models.ads_zone import AdsZone
from controllers.base_controller import BaseController
from models.ads_zone_format import AdsZoneFormat


class AdsZoneController(BaseController):
    def post(self):
        try:
            data = request.get_json()

            # Tạo instance AdsZone với dữ liệu từ request
            ads_zone = AdsZone(
                website_id=data.get('website_id'),
                ten_vung_quang_cao=data.get('ten_vung_quang_cao'),
                size_id=data.get('size_id'),
                formats=data.get('formats', [])
            )

            # Lưu vùng quảng cáo và các định dạng
            zone_id = ads_zone.save()

            return {
                'success': True,
                'message': 'Vùng quảng cáo đã được tạo thành công',
                'zone_id': zone_id
            }, 201

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 400

    def get(self, ads_zone_id=None):
        params = request.args
        if ads_zone_id:
            if request.path.endswith('/formats'):
                # Get formats for specific zone
                formats = AdsZoneFormat.get_by_zone_id(ads_zone_id)
                return jsonify({'formats': formats})
            else:
                ads_zone = AdsZone.get_by_id(ads_zone_id)
                return jsonify(ads_zone)
        elif params.get('website_id'):
            ads_zones = AdsZone.get_by_website_id(params.get('website_id'))
            return jsonify({'ads_zones': ads_zones})
        else:
            ads_zones = AdsZone.get_all()
            return jsonify({'ads_zones': ads_zones})

    def delete(self, ads_zone_id):
        AdsZone.delete_by_id(ads_zone_id)
        return jsonify({'message': 'Vùng quảng cáo đã được xóa thành công'})

    def put(self, ads_zone_id):
        data = request.get_json()
        AdsZone.update(ads_zone_id, data)
        return jsonify({'message': 'Vùng quảng cáo đã được cập nhật thành công'})
