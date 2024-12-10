from flask import request
from flask_restful import Resource, fields, marshal_with
import base64

from models.data_source import DataSource

data_source_fields = {
    'data_source_id': fields.Integer,
    'ten_nguon': fields.String,
    'filename': fields.String,
    'file': fields.String,  # Will store base64 encoded string
    'user_id': fields.Integer,
    'username': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'active': fields.Boolean
}


class DataSourceController(Resource):
    @marshal_with(data_source_fields)
    def get(self, source_id=None):
        try:
            if source_id:
                data = DataSource.get_by_id(source_id)
            else:
                data = DataSource.get_all()

            # Convert binary data to base64 string
            if isinstance(data, list):
                for item in data:
                    if item.get('file'):
                        item['file'] = base64.b64encode(
                            item['file']).decode('utf-8')
            elif data and data.get('file'):
                data['file'] = base64.b64encode(data['file']).decode('utf-8')

            return data
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            if 'file' in data and isinstance(data['file'], str):
                data['file'] = base64.b64decode(data['file'])
            source = DataSource(**data)
            source.save()
            return {'message': 'Data source created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

    def put(self, source_id):
        try:
            data = request.get_json()
            if 'file' in data and isinstance(data['file'], str):
                data['file'] = base64.b64decode(data['file'])
            source = DataSource(**data)
            source.source_id = source_id
            source.update()
            return {'message': 'Data source updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, source_id):
        try:
            DataSource.delete(source_id)
            return {'message': 'Data source deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400
