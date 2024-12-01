from flask import jsonify, request
from flask_restful import Resource
from models.city import City


class CityController(Resource):
    def get(self, city_id=None):
        try:
            if city_id:
                city = City.get_by_id(city_id)
                return jsonify(city)
            cities = City.get_all()
            return jsonify(cities)
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

    def post(self):
        try:
            data = request.get_json()
            city = City(
                ten_thanh_pho=data.get('ten_thanh_pho'),
                country_id=data.get('country_id'),
                mien=data.get('mien')
            )
            city.create()
            return jsonify({
                'status': 'success',
                'message': 'Thành phố đã được tạo thành công'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

    def put(self, city_id):
        try:
            data = request.get_json()
            city = City(
                city_id=city_id,
                ten_thanh_pho=data.get('ten_thanh_pho'),
                country_id=data.get('country_id'),
                mien=data.get('mien')
            )
            city.update()
            return jsonify({
                'status': 'success',
                'message': 'Cập nhật thành phố thành công'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

    @staticmethod
    def delete_city(city_id):
        try:
            City.delete_by_id(city_id)
            return jsonify({
                'status': 'success',
                'message': 'Xóa thành phố thành công'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })
