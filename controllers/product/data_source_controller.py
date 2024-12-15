from flask import request, jsonify
from flask_restful import Resource
import base64
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from models.source_status import SourceStatus
from models.product import Product
from models.data_source import DataSource
from controllers.base_controller import BaseController
from configs.db import get_db_connection


class DataSourceController(BaseController):
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    UPLOAD_FOLDER = 'uploads/excel'

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def get(self, source_id=None):
        try:
            if source_id:
                data = DataSource.get_by_id(source_id)
                if not data:
                    return jsonify({'message': 'Data source not found'}), 404
                
                response = {
                    'source_id': data['source_id'],
                    'ten_nguon_du_lieu': data['ten_nguon_du_lieu'],
                    'trang_thai': data['ten_trang_thai'],
                    'updated_at': data['updated_at'].strftime('%d/%m/%Y %H:%M:%S') if data['updated_at'] else None,
                    'so_san_pham': data['total_products'] or 0
                }
                return jsonify({
                    'message': 'Data source retrieved successfully',
                    'data': response
                })
            else:
                data = DataSource.get_all()
                response = []
                for idx, item in enumerate(data, 1):
                    response.append({
                        'stt': idx,
                        'source_id': item['source_id'],
                        'ten_nguon_du_lieu': item['ten_nguon_du_lieu'],
                        'trang_thai': item['ten_trang_thai'],
                        'updated_at': item['updated_at'].strftime('%d/%m/%Y %H:%M:%S') if item['updated_at'] else None,
                        'so_san_pham': item['total_products'] or 0
                    })
                return jsonify({
                    'message': 'Data sources retrieved successfully',
                    'data': response
                })
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    def post(self):
        try:
            if 'file' not in request.files:
                return jsonify({'message': 'No file uploaded'}), 400

            file = request.files['file']
            name = request.form.get('ten_nguon_du_lieu')

            if not name:
                return jsonify({'message': 'Name is required'}), 400

            if file.filename == '':
                return jsonify({'message': 'No file selected'}), 400

            if not self.allowed_file(file.filename):
                return jsonify({'message': 'File type not allowed'}), 400

            # Save file with secure name
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            file_path = os.path.join(self.UPLOAD_FOLDER, filename)
            os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

            try:
                file.save(file_path)
            except Exception as e:
                return jsonify({'message': f'Error saving file: {str(e)}'}), 400

            # Create data source with PENDING status
            try:
                source = DataSource(
                    ten_nguon_du_lieu=name,
                    duong_dan_file=file_path,
                    status_id=DataSource.get_status_id('Đang chờ xử lý')
                )
                source_id = source.save()
            except Exception as e:
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({'message': f'Error creating data source: {str(e)}'}), 400

            # Process file in background
            try:
                self.process_excel_file(source_id, file_path)
            except Exception as e:
                return jsonify({'message': f'Error processing file: {str(e)}'}), 400

            return jsonify({
                'message': 'Data source created successfully',
                'source_id': source_id
            }), 201

        except Exception as e:
            return jsonify({'message': str(e)}), 400

    def process_excel_file(self, source_id, file_path):
        try:
            # Update status to PROCESSING
            DataSource.update_source_status(source_id, 'Đang xử lý')

            # Read Excel file
            df = pd.read_excel(file_path)

            # Required columns mapping
            required_columns = {
                'tiêu đề': 'ten_san_pham',  # Tên sản phẩm
                'mô tả': 'mo_ta_san_pham',  # Mô tả sản phẩm
                'liên kết': 'lien_ket_san_pham',  # Link sản phẩm 
                'giá': 'gia_san_pham',  # Giá gốc
                'còn hàng': 'tinh_trang_con_hang', # Trạng thái tồn kho
                'liên kết hình ảnh': 'lien_ket_hinh_anh' # Link hình ảnh
            }

            # Validate required columns
            missing_columns = [col for col in required_columns.keys() if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

            # Rename columns
            df = df.rename(columns=required_columns)

            valid_products = 0
            error_products = 0

            # Process each row
            for index, row in df.iterrows():
                try:
                    # Basic validation
                    if not row.get('ten_san_pham') or not row.get('lien_ket_san_pham'):
                        error_products += 1
                        continue

                    # Convert price values
                    try:
                        gia_san_pham = float(row.get('gia_san_pham', 0))
                    except (ValueError, TypeError):
                        gia_san_pham = 0
                    
                    # Convert stock status
                    tinh_trang_con_hang = row.get('tinh_trang_con_hang', '').lower() == 'còn hàng'
                    
                    # Create product with default values
                    product = Product(
                        ten_san_pham=row.get('ten_san_pham'),
                        mo_ta_san_pham=row.get('mo_ta_san_pham', ''),
                        luot_xem=0,
                        luot_nhan=0,
                        ctr=0.0,
                        so_luong_mua_hang=0,
                        phan_tram_chuyen_doi_mua_hang=0.0,
                        lien_ket_san_pham=row.get('lien_ket_san_pham'),
                        hinh_anh_san_pham=None,  # Binary data will be added later if needed
                        lien_ket_hinh_anh=row.get('lien_ket_hinh_anh'),
                        source_id=source_id,
                        productstatus_id=1 if tinh_trang_con_hang else 2,  # 1: Active, 2: Inactive
                        gia_san_pham=gia_san_pham,
                        gia_khuyen_mai=None,
                        active=True
                    )
                    product.save()
                    valid_products += 1
                    
                except Exception as e:
                    error_products += 1
                    print(f"Error processing row {index}: {str(e)}")

            # Update source with product counts
            DataSource.update_source_products(source_id, valid_products, error_products)

            # Update status to COMPLETED
            DataSource.update_source_status(source_id, 'Đã xử lý')

        except Exception as e:
            print(f"Error processing file: {str(e)}")
            DataSource.update_source_status(source_id, 'Lỗi')
            raise

        finally:
            # Remove file after processing
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing file: {str(e)}")

    def put(self, source_id):
        try:
            data = request.get_json()
            source = DataSource.get_by_id(source_id)
            if not source:
                return jsonify({'message': 'Data source not found'}), 404

            # Update source
            source.ten_nguon_du_lieu = data.get('ten_nguon_du_lieu', source.get('ten_nguon_du_lieu'))
            source.status_id = data.get('status_id', source.get('status_id'))
            source.update()

            return jsonify({'message': 'Data source updated successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    def delete(self, source_id):
        try:
            DataSource.delete(source_id)
            return jsonify({'message': 'Data source deleted successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400
