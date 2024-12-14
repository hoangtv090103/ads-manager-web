from flask import request, jsonify
from controllers.base_controller import BaseController
from models.ads_zone_size import AdsZoneSize


class AdsZoneSizeController(BaseController):
    def get(self, size_id=None):
        try:
            if size_id:
                size = AdsZoneSize.get_by_size_id(size_id)
                if not size:
                    return jsonify({"error": "Ad zone size not found"}), 404
                return jsonify({"size": size})
            
            sizes = AdsZoneSize.get_all()
            return jsonify({"sizes": sizes})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            required_fields = ['ten_kich_thuoc']
            
            # Validate required fields
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            ads_zone_size = AdsZoneSize(**data)
            ads_zone_size.save()
            
            return jsonify({
                "message": "Ad zone size created successfully"
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, size_id):
        try:
            data = request.get_json()
            
            # Check if size exists
            existing_size = AdsZoneSize.get_by_size_id(size_id)
            if not existing_size:
                return jsonify({"error": "Ad zone size not found"}), 404

            # Update size
            ads_zone_size = AdsZoneSize(**data)
            ads_zone_size.size_id = size_id
            ads_zone_size.update()
            
            return jsonify({
                "message": "Ad zone size updated successfully"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, size_id):
        try:
            # Check if size exists
            existing_size = AdsZoneSize.get_by_size_id(size_id)
            if not existing_size:
                return jsonify({"error": "Ad zone size not found"}), 404

            AdsZoneSize.delete_by_id(size_id)
            return jsonify({
                "message": "Ad zone size deleted successfully"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500 