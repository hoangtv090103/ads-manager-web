from flask import request
from flask_restful import Resource, fields, marshal_with
import base64

from models.data_source import DataSource
from controllers.base_controller import BaseController


class DataSourceController(BaseController):
    def get(self, source_id=None):
        try:
            if source_id:
                data = DataSource.get_by_id(source_id)
            else:
                data = DataSource.get_all()

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
