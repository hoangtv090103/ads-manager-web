from flask import request
from flask_restful import Resource, fields, marshal_with

from controllers.base_controller import BaseController
from models.target_audience_status import TargetAudienceStatus
import logging

_logger = logging.getLogger(__name__)

target_audience_status_fields = {
    'ta_status_id': fields.Integer,
    'ten_trang_thai': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'active': fields.Boolean
}


class TargetAudienceStatusController(BaseController):
    @marshal_with(target_audience_status_fields)
    def get(self, status_id=None):
        try:
            if status_id:
                return TargetAudienceStatus.get_by_id(status_id)
            return TargetAudienceStatus.get_all()
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:

            data = request.get_json()
            status = TargetAudienceStatus(
                ten_trang_thai=data.get('ten_trang_thai')
            )
            status.create()
            return {"message": "Status created successfully"}, 201
        except Exception as e:
            _logger.error(f"Error creating status: {str(e)}")
            return {"message": str(e)}, 500

    def put(self, status_id):
        try:
            data = request.get_json()
            status = TargetAudienceStatus(**data)
            status.ta_status_id = status_id
            status.update()
            return {'message': 'Target audience status updated successfully'}, 200
        except Exception as e:
            _logger.error(f"Error updating target audience status: {str(e)}")
            return {'message': str(e)}, 400

    def delete(self, status_id):
        try:
            TargetAudienceStatus.delete_by_id(status_id)
            return {'message': 'Target audience status deleted successfully'}, 200
        except Exception as e:
            _logger.error(f"Error deleting target audience status: {str(e)}")
            return {'message': str(e)}, 400
