from flask import request, jsonify
from controllers.base_controller import BaseController
from models.campaign_type import CampaignType

class CampaignTypeController(BaseController):
    def get(self, type_id=None):
        try:
            if type_id:
                campaign_type = CampaignType.get_by_id(type_id)
                return jsonify({"campaign_type": campaign_type})
            campaign_types = CampaignType.get_all()
            return jsonify({"campaign_types": campaign_types})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 