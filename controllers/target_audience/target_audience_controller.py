from flask import request, jsonify
from flask_restful import Resource
from models.target_audience import TargetAudience
import logging

_logger = logging.getLogger(__name__)


class TargetAudienceController(Resource):
    def get(self, ta_id=None):
        try:
            if ta_id:
                target = TargetAudience.get_by_id(ta_id)
                if target:
                    return jsonify({"status": "success", "data": target})
                return {"message": "Target audience not found"}, 404

            targets = TargetAudience.get_all()
            return jsonify({"status": "success", "data": targets})
        except Exception as e:
            _logger.error(f"Error fetching target audiences: {str(e)}")
            return {"message": str(e)}, 500

    def post(self):
        try:
            data = request.get_json()
            target = TargetAudience(
                ten_nhom_doi_tuong=data.get('ten_nhom_doi_tuong'),
                ta_status_id=data.get('ta_status_id', 1),  # Default status
                trang_da_truy_cap=data.get('trang_da_truy_cap'),
                hanh_vi_khach_hang=data.get('hanh_vi_khach_hang')
            )
            target.create()
            return {"message": "Target audience created successfully"}, 201
        except Exception as e:
            _logger.error(f"Error creating target audience: {str(e)}")
            return {"message": str(e)}, 500

    def put(self, ta_id):
        try:
            data = request.get_json()
            target = TargetAudience(
                ta_id=ta_id,
                ten_nhom_doi_tuong=data.get('ten_nhom_doi_tuong'),
                ta_status_id=data.get('ta_status_id'),
                trang_da_truy_cap=data.get('trang_da_truy_cap'),
                hanh_vi_khach_hang=data.get('hanh_vi_khach_hang')
            )
            target.update()
            return {"message": "Target audience updated successfully"}
        except Exception as e:
            _logger.error(f"Error updating target audience: {str(e)}")
            return {"message": str(e)}, 500

    def delete(self, ta_id):
        try:
            TargetAudience.delete_by_id(ta_id)
            return {"message": "Target audience deleted successfully"}
        except Exception as e:
            _logger.error(f"Error deleting target audience: {str(e)}")
            return {"message": str(e)}, 500
