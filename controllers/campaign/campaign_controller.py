from flask import request, jsonify
from controllers.base_controller import BaseController
from models.campaign import Campaign
from middlewares.auth_middleware import token_required
from controllers.base_controller import BaseController
class CampaignController(BaseController):
    def get(self, camp_id=None):
        try:
            if camp_id:
                campaign = Campaign.get_by_id(camp_id)
                return jsonify({"campaign": campaign})
            campaigns = Campaign.get_all()
            return jsonify({"campaigns": campaigns})
        except Exception as e:
            return jsonify({"error": str(e)})

    def post(self):
        try:
            data = request.json
            campaign = Campaign(**data)
            campaign.create()   
            return jsonify({"message": "Campaign created successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def put(self, camp_id):
        try:
            data = request.json
            Campaign.update(camp_id, data)
            return jsonify({"message": "Campaign updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def delete(self, camp_id):
        try:
            Campaign.delete(camp_id)
            return jsonify({"message": "Campaign deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})