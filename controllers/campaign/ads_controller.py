from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_restful import Resource
from models.ads import Ads


class AdsController(Resource):
    def get(self, ads_id=None):
        try:
            if ads_id:
                ads = Ads.get_by_id(ads_id)
                return jsonify(ads)
            ads_list = Ads.get_all()
            return jsonify(ads_list)
        except Exception as e:
            return jsonify({"error": str(e)})

    def post(self):
        try:
            # Lấy thông tin cơ bản
            data = {
                'ten_tin_quang_cao': request.form.get('name'),
                'URL_dich': request.form.get('target_url'),
                'format_type': request.form.get('format_type')
            }
            
            # Xử lý file upload nếu có
            if 'resource' in request.files:
                file = request.files['resource']
                if file:
                    filename = secure_filename(file.filename)
                    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'ads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    data['resource_path'] = file_path

            # Tạo quảng cáo mới
            ads = Ads(**data)
            ads.create()
            
            return jsonify({"message": "Advertisement created successfully"}), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def put(self, ads_id):
        try:
            data = request.json
            ads = Ads(**data)
            ads.ads_id = ads_id
            ads.update()
            return jsonify({"message": "Advertisement updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)})
