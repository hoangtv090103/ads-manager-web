from flask import request, jsonify
from controllers.base_controller import BaseController
from models.publisher import Publisher
from middlewares.auth_middleware import token_required


class PublisherController(BaseController):
    def get(self, publisher_id=None):
        try:
            if publisher_id:
                publisher = Publisher.get_by_id(publisher_id)
                return jsonify({"publisher": publisher})
            publishers = Publisher.get_all()
            return jsonify({"publishers": publishers})
        except Exception as e:
            return jsonify({"error": str(e)})

    def post(self):
        try:
            data = request.json
            publisher = Publisher(**data)
            publisher.save()
            return jsonify({"message": "Publisher created successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def put(self, publisher_id):
        try:
            data = request.json
            publisher = Publisher(**data)
            publisher.publisher_id = publisher_id
            publisher.update()
            return jsonify({"message": "Publisher updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def delete(self, publisher_id):
        try:
            Publisher.delete_by_id(publisher_id)
            return jsonify({"message": "Publisher deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})
