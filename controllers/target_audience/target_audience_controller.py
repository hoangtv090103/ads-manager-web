from flask import request, jsonify
from flask_restful import Resource
from controllers.base_controller import BaseController
from models.behaviour import Behaviour
from models.target_audience import TargetAudience


class TargetAudienceController(BaseController):
    def get(self, ta_id=None):
        try:
            if ta_id:
                target = TargetAudience.get_by_id(ta_id)
                if not target:
                    return jsonify({'success': False, 'message': 'Target audience not found'}), 404
                return jsonify({'success': True, 'target_audience': target})
            else:
                targets = TargetAudience.get_all()
                return jsonify({'success': True, 'target_audiences': targets})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = ['ten_nhom_doi_tuong']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'message': f'Missing required field: {field}'}, 400
            if data.get('behaviors'):
                HanhViID = Behaviour.get_by_id(
                    data.get('behaviors')[0].get('behavior_id')).get('behav_id')
                LoaiTruHanhViID = Behaviour.get_by_id(
                    data.get('behaviors')[len(data.get('behaviors')) - 1].get('behavior_id')).get('behav_id')
            else:
                HanhViID = None
                LoaiTruHanhViID = None

            # Create new target audience
            target = TargetAudience(
                ten_nhom_doi_tuong=data.get('ten_nhom_doi_tuong'),
                trang_da_truy_cap=data.get('trang_da_truy_cap', ''),
                apply_all_product=data.get('apply_all_product', False),
                HanhViID=HanhViID,
                LoaiTruHanhViID=LoaiTruHanhViID
            )

            ta_id = target.create()
            return {
                'success': True,
                'message': 'Target audience created successfully',
                'ta_id': ta_id
            }, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

    def put(self, ta_id):
        try:
            data = request.get_json()

            # Check if target audience exists
            existing_target = TargetAudience.get_by_id(ta_id)
            if not existing_target:
                return {'success': False, 'message': 'Target audience not found'}, 404

            # Update target audience
            target = TargetAudience(
                ta_id=ta_id,
                ten_nhom_doi_tuong=data.get(
                    'ten_nhom_doi_tuong', existing_target['ten_nhom_doi_tuong']),
                trang_da_truy_cap=data.get(
                    'trang_da_truy_cap', existing_target['trang_da_truy_cap']),
                apply_all_product=data.get(
                    'apply_all_product', existing_target['apply_all_product']),
                product_info=data.get('product_info', {}),
                behaviors=data.get('behaviors', [])
            )

            target.update()
            return {'success': True, 'message': 'Target audience updated successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

    def delete(self, ta_id):
        try:
            # Check if target audience exists
            existing_target = TargetAudience.get_by_id(ta_id)
            if not existing_target:
                return {'success': False, 'message': 'Target audience not found'}, 404

            TargetAudience.delete_by_id(ta_id)
            return {'success': True, 'message': 'Target audience deleted successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
