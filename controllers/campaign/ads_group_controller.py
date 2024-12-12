from flask import request, jsonify
from flask_restful import Resource
from controllers.base_controller import BaseController
from models.ads_group import AdsGroup

class AdsGroupController(BaseController):
    def get(self, ads_group_id=None):
        try:
            if ads_group_id:
                ads_group = AdsGroup.get_by_id(ads_group_id)
                return jsonify(ads_group)
            ads_groups = AdsGroup.get_all()
            return jsonify(ads_groups)
        except Exception as e:
            return jsonify({"error": str(e)})

    def post(self):
        try:
            data = request.json
            ads_group = AdsGroup(**data)
            ads_group.save()
            return jsonify({"message": "Ads group created successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def put(self, ads_group_id):
        try:
            data = request.json
            ads_group = AdsGroup(**data)
            ads_group.ads_group_id = ads_group_id
            ads_group.update()
            return jsonify({"message": "Ads group updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})
