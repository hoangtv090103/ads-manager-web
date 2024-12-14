from flask import request, jsonify
from models.behaviour import Behaviour
from controllers.base_controller import BaseController


class BehaviourController(BaseController):
    def get(self, behav_id=None):
        """Get all behaviours"""
        try:
            if behav_id:
                behaviours = Behaviour.get_by_id(behav_id)
            else:
                behaviours = Behaviour.get_all()
            return jsonify({
                'status': 'success',
                'behaviours': behaviours
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

    def post(self):
        """Create a new behaviour"""
        try:
            data = request.get_json()
            behaviour = Behaviour(ten_hanh_vi=data['ten_hanh_vi'])
            behav_id = behaviour.create()
            return jsonify({
                'status': 'success',
                'message': 'Behaviour created successfully',
                'data': {'behav_id': behav_id}
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

    def put(self, behav_id):
        """Update a behaviour"""
        try:
            data = request.get_json()
            behaviour = Behaviour(behav_id=behav_id, ten_hanh_vi=data['ten_hanh_vi'])
            behaviour.update()
            return jsonify({
                'status': 'success',
                'message': 'Behaviour updated successfully'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

    def delete(self, behav_id):
        """Delete a behaviour"""
        try:
            behaviour = Behaviour(behav_id=behav_id)
            behaviour.delete()
            return jsonify({
                'status': 'success',
                'message': 'Behaviour deleted successfully'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })
