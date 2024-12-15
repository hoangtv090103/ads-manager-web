from flask import request, jsonify
from controllers.base_controller import BaseController
from models.ads_group import AdsGroup
from models.ads_group_website import AdsGroupWebsite
from models.ads_group_target_audience import AdsGroupTargetAudience
from models.ads_group_product_group_mapping import AdsGroupProductGroupMapping
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
                    return {"error": "Ads group not found"}, 404
                return {"ads_group": ads_group}

            logger.debug("Fetching all ads groups")
            ads_groups = AdsGroup.get_all()
            logger.debug(
                f"Found {len(ads_groups) if ads_groups else 0} ads groups")

            if not ads_groups:
                logger.warning("No ads groups found in database")
                return {"ads_groups": []}

            logger.debug("Successfully processed all ads groups")
            return {"ads_groups": ads_groups}
        except Exception as e:
            logger.error(f"Error in get ads groups: {str(e)}", exc_info=True)
            return {"error": str(e)}, 500

    def post(self):
        try:
            data = request.json
            logger.debug(f"Received POST request with data: {data}")

            # Create ads group
            ads_group = AdsGroup(
                camp_id=data.get('camp_id'),
                ads_group_status_id=1,  # Default status
                ten_nhom=data.get('ten_nhom'),
                nham_chon_all_san_pham=data.get(
                    'nham_chon_all_san_pham', False),
                nham_chon_doi_tuong=data.get('nham_chon_doi_tuong', False),
                nham_chon_dia_ly=data.get('nham_chon_dia_ly', ''),
                gioi_tinh_khong_xac_dinh=data.get(
                    'gioi_tinh_khong_xac_dinh', False),
                gioi_tinh_nam=data.get('gioi_tinh_nam', False),
                gioi_tinh_nu=data.get('gioi_tinh_nu', False),
                tuoi_less_than_18=data.get('tuoi_less_than_18', False),
                tuoi_from_18_to_24=data.get('tuoi_from_18_to_24', False),
                tuoi_from_25_to_34=data.get('tuoi_from_25_to_34', False),
                tuoi_from_35_to_50=data.get('tuoi_from_35_to_50', False),
                tuoi_more_than_50=data.get('tuoi_more_than_50', False)
            )
            ads_group_id = ads_group.save()
            logger.debug(f"Created ads group with ID: {ads_group_id}")

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

            return {
                "message": "Ads group created successfully",
                "ads_group_id": ads_group_id
            }, 201
        except Exception as e:
            logger.error(f"Error creating ads group: {str(e)}", exc_info=True)
            return {"error": str(e)}, 500

    def put(self, ads_group_id):
        try:
            data = request.json
            ads_group = AdsGroup(**data)
            ads_group.ads_group_id = ads_group_id
            ads_group.update()
            return {"message": "Ads group updated successfully"}
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, ads_group_id):
        try:
            AdsGroup.delete_by_id(ads_group_id)
            return {"message": "Ads group deleted successfully"}
        except Exception as e:
            return {"error": str(e)}, 500
