from flask import request, jsonify
from controllers.base_controller import BaseController
from models.ads_group import AdsGroup
from models.ads_group_website import AdsGroupWebsite
from models.ads_group_target_audience import AdsGroupTargetAudience
from models.ads_group_product_group_mapping import AdsGroupProductGroupMapping
from models.remarketing_setting import RemarketingSetting
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AdsGroupController(BaseController):
    def get(self, ads_group_id=None):
        try:
            logger.debug("Starting get request for ads groups")
            if ads_group_id:
                logger.debug(
                    f"Fetching single ads group with ID: {ads_group_id}")
                ads_group = AdsGroup.get_by_id(ads_group_id)
                if not ads_group:
                    return jsonify({"error": "Ads group not found"})
                return jsonify({"ads_group": ads_group})

            logger.debug("Fetching all ads groups")
            ads_groups = AdsGroup.get_all()
            logger.debug(
                f"Found {len(ads_groups) if ads_groups else 0} ads groups")

            if not ads_groups:
                logger.warning("No ads groups found in database")
                return jsonify({"ads_groups": []})

            logger.debug("Successfully processed all ads groups")
            return jsonify({"ads_groups": ads_groups})
        except Exception as e:
            logger.error(f"Error in get ads groups: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)})

    def post(self):
        try:
            data = request.json
            logger.debug(f"Received POST request with data: {data}")

            # 1. Tạo nhóm quảng cáo cơ bản
            ads_group = AdsGroup(
                camp_id=data.get('camp_id'),
                ads_group_status_id=1,  # Trạng thái mặc định
                ten_nhom=data.get('ten_nhom'),
                nham_chon_all_san_pham=data.get('nham_chon_all_san_pham', False),
                nham_chon_doi_tuong=data.get('nham_chon_doi_tuong', False),
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

            # 2. Xử lý website được chọn
            websites = data.get('websites', [])
            for website_id in websites:
                website_mapping = AdsGroupWebsite(
                    ads_group_id=ads_group_id,
                    website_id=website_id
                )
                website_mapping.create()

            # 3. Xử lý remarketing settings nếu có
            remarketing_data = data.get('remarketing_settings')
            if remarketing_data:
                remarketing = RemarketingSetting(
                    ads_group_id=ads_group_id,
                    auto_remarketing=remarketing_data.get('auto_remarketing', False),
                    tan_suat_hien_thi=remarketing_data.get('tan_suat_hien_thi', 0),
                    thoi_gian_giua_hai_lan_hien_thi=remarketing_data.get('thoi_gian_giua_hai_lan_hien_thi', 0),
                    thoi_gian_remarketing=remarketing_data.get('thoi_gian_remarketing', 0),
                    stop_on_click=remarketing_data.get('stop_on_click', False),
                    stop_on_view=remarketing_data.get('stop_on_view', False),
                    max_view=remarketing_data.get('max_view', 0)
                )
                remarketing.create()

            # 4. Xử lý nhóm sản phẩm
            if not data.get('nham_chon_all_san_pham'):
                product_group_id = data.get('product_group_id')
                if product_group_id:
                    product_group_mapping = AdsGroupProductGroupMapping(
                        ads_group_id=ads_group_id,
                        product_group_id=product_group_id
                    )
                    product_group_mapping.create()

            # 5. Xử lý nhóm đối tượng
            if data.get('nham_chon_doi_tuong'):
                target_audience_id = data.get('target_audience_id')
                if target_audience_id:
                    ta_mapping = AdsGroupTargetAudience(
                        ads_group_id=ads_group_id,
                        ta_id=target_audience_id
                    )
                    ta_mapping.create()

            return jsonify({
                "message": "Ads group created successfully",
                "ads_group_id": ads_group_id
            })

        except Exception as e:
            logger.error(f"Error creating ads group: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)})

    def put(self, ads_group_id):
        try:
            data = request.json
            ads_group = AdsGroup(**data)
            ads_group.ads_group_id = ads_group_id
            ads_group.update()
            return jsonify({"message": "Ads group updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def delete(self, ads_group_id):
        try:
            AdsGroup.delete_by_id(ads_group_id)
            return jsonify({"message": "Ads group deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})
