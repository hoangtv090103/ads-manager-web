
from flask import jsonify, request
from controllers.base_controller import BaseController
from models.ads import Ads

class AdsController(BaseController):
    def get(self):
        try:
            ads_list = Ads.get_all()
            return jsonify({
                "success": True,
                "ads": ads_list
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    def put(self, ads_id):
        try:
            data = request.get_json()
            active = data.get('active')
            
            if active is None:
                return jsonify({
                    "success": False,
                    "error": "Active status is required"
                }), 400

            success = Ads.update_ads_status(ads_id, active)
            
            if not success:
                return jsonify({
                    "success": False,
                    "error": "Ad not found"
                }), 404

            return jsonify({
                "success": True,
                "message": "Ad status updated successfully"
            })

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500 