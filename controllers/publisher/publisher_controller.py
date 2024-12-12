from flask import request, jsonify
from controllers.base_controller import BaseController
from models.publisher import Publisher

class PublisherController(BaseController):
    def get(self, publisher_id=None):
        try:
            if publisher_id:
                publisher = Publisher.get_by_id(publisher_id)
                if not publisher:
                    return jsonify({"error": "Publisher not found"}), 404
                return jsonify({"publisher": publisher})
            
            publishers = Publisher.get_all()
            return jsonify({"publishers": publishers})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.json
            required_fields = ['ten_publisher', 'email', 'user_id']
            
            # Validate required fields
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            publisher = Publisher(**data)
            publisher.save()
            return jsonify({
                "message": "Publisher created successfully",
                "publisher_id": publisher.publisher_id
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, publisher_id):
        try:
            data = request.json
            publisher = Publisher.get_by_id(publisher_id)
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 404
            
            for key, value in data.items():
                setattr(publisher, key, value)
            publisher.update()
            
            return jsonify({"message": "Publisher updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, publisher_id):
        try:
            Publisher.delete_by_id(publisher_id)
            return jsonify({"message": "Publisher deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
