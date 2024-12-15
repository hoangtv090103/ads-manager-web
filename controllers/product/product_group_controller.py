from flask import request, jsonify
from flask_restful import Resource
from models.product_group import ProductGroup
from controllers.base_controller import BaseController
from models.product import Product

class ProductGroupController(BaseController):
    def get(self, group_id=None):
        try:
            if group_id:
                group = ProductGroup.get_by_id(group_id)
                if not group:
                    return jsonify({
                        'message': 'Không tìm thấy nhóm sản phẩm',
                        'data': None
                    }), 404
                return jsonify({
                    'message': 'Lấy thông tin nhóm sản phẩm thành công',
                    'data': group
                })
            else:
                groups = ProductGroup.get_all()
                return jsonify({
                    'message': 'Lấy danh sách nhóm sản phẩm thành công',
                    'data': groups
                })
        except Exception as e:
            return jsonify({
                'message': str(e),
                'data': None
            })

    def post(self):
        try:
            data = request.get_json()
            group = ProductGroup(
                ten_nhom=data.get('ten_nhom'),
                source_id=data.get('source_id'),
                phan_loai_theo=data.get('phan_loai_theo'),
                products=data.get('products', [])
            )
            group_id = group.save()
            return jsonify({
                'message': 'Tạo nhóm sản phẩm thành công',
                'data': {'productgroup_id': group_id}
            })
        except Exception as e:
            return jsonify({
                'message': str(e),
                'data': None
            })

    def put(self, group_id):
        try:
            data = request.get_json()
            group = ProductGroup(
                productgroup_id=group_id,
                ten_nhom=data.get('ten_nhom'),
                source_id=data.get('source_id'),
                phan_loai_theo=data.get('phan_loai_theo'),
                products=data.get('products', [])
            )
            group.update()
            return jsonify({
                'message': 'Cập nhật nhóm sản phẩm thành công',
                'data': None
            })
        except Exception as e:
            return jsonify({
                'message': str(e),
                'data': None
            })

    def delete(self, group_id):
        try:
            ProductGroup.delete(group_id)
            return jsonify({
                'message': 'Xóa nhóm sản phẩm thành công',
                'data': None
            })
        except Exception as e:
            return jsonify({
                'message': str(e),
                'data': None
            })

    @staticmethod
    def get_product_fields():
        """Get all available fields from Product model for classification"""
        fields = [
            {'field': 'ten_san_pham', 'label': 'Tên sản phẩm'},
            {'field': 'mo_ta_san_pham', 'label': 'Mô tả sản phẩm'},
            {'field': 'lien_ket_san_pham', 'label': 'Liên kết sản phẩm'},
            {'field': 'gia_san_pham', 'label': 'Giá sản phẩm'},
            {'field': 'tinh_trang_con_hang', 'label': 'Trạng thái tồn kho'},
            {'field': 'lien_ket_hinh_anh', 'label': 'Liên kết hình ảnh'},
            {'field': 'luot_xem', 'label': 'Lượt xem'},
            {'field': 'luot_nhan', 'label': 'Lượt nhấn'},
            {'field': 'ctr', 'label': 'CTR'},
            {'field': 'so_luong_mua_hang', 'label': 'Số lượng mua hàng'},
            {'field': 'phan_tram_chuyen_doi_mua_hang', 'label': 'Phần trăm chuyển đổi'}
        ]
        return jsonify({
            'message': 'Lấy danh sách trường phân loại thành công',
            'data': fields
        })
