from flask import request, jsonify
from flask_restful import Resource
from controllers.base_controller import BaseController
from models.ads_group import AdsGroup
from models.ads_group_website import AdsGroupWebsite
from models.ads_group_target_audience import AdsGroupTargetAudience
from models.ads_group_product_group_mapping import AdsGroupProductGroupMapping

class AdsGroupController(BaseController):
    def get(self, ads_group_id=None):
        try:
            if ads_group_id:
                ads_group = AdsGroup.get_by_id(ads_group_id)
                return jsonify({"ads_group": ads_group})
            ads_groups = AdsGroup.get_all()
            return jsonify({"ads_groups": ads_groups})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.json
            
            # Create ads group
            ads_group = AdsGroup(
                camp_id=data.get('camp_id'),
                ads_group_status_id=1,  # Default status
                ten_nhom=data.get('ten_nhom'),
                nham_chon_all_san_pham=data.get('nham_chon_all_san_pham', False),
                nham_chon_doi_tuong=data.get('nham_chon_doi_tuong', False),
                nham_chon_dia_ly=data.get('nham_chon_dia_ly', ''),
                gioi_tinh_khong_xac_dinh=data.get('gioi_tinh_khong_xac_dinh', False),
                gioi_tinh_nam=data.get('gioi_tinh_nam', False),
                gioi_tinh_nu=data.get('gioi_tinh_nu', False),
                tuoi_less_than_18=data.get('tuoi_less_than_18', False),
                tuoi_from_18_to_24=data.get('tuoi_from_18_to_24', False),
                tuoi_from_25_to_34=data.get('tuoi_from_25_to_34', False),
                tuoi_from_35_to_50=data.get('tuoi_from_35_to_50', False),
                tuoi_more_than_50=data.get('tuoi_more_than_50', False)
            )
            ads_group_id = ads_group.save()

            # Create website mappings
            websites = data.get('websites', [])
            for website_id in websites:
                website_mapping = AdsGroupWebsite(
                    ads_group_id=ads_group_id,
                    website_id=website_id
                )
                website_mapping.create()

            # Create target audience mappings
            target_audiences = data.get('target_audiences', [])
            for ta_id in target_audiences:
                ta_mapping = AdsGroupTargetAudience(
                    ads_group_id=ads_group_id,
                    ta_id=ta_id
                )
                ta_mapping.create()

            # Create product group mappings
            product_groups = data.get('product_groups', [])
            for product_group_id in product_groups:
                pg_mapping = AdsGroupProductGroupMapping(
                    product_group_id=product_group_id
                )
                pg_mapping.create()

            return jsonify({
                "message": "Ads group created successfully",
                "ads_group_id": ads_group_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, ads_group_id):
        try:
            data = request.json
            ads_group = AdsGroup(**data)
            ads_group.ads_group_id = ads_group_id
            ads_group.update()
            return jsonify({"message": "Ads group updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, ads_group_id):
        try:
            AdsGroup.delete_by_id(ads_group_id)
            return jsonify({"message": "Ads group deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
