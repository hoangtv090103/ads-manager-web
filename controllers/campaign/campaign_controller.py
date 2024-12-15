from datetime import datetime
from flask import request, jsonify
from controllers.base_controller import BaseController
from models.campaign import Campaign
from models.campaign_status import CampStatus
from models.campaign_type import CampaignType
from controllers.base_controller import BaseController
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CampaignController(BaseController):
    def get(self, camp_id=None):
        try:
            logger.debug("Starting get request for campaigns")
            if camp_id:
                logger.debug(f"Fetching single campaign with ID: {camp_id}")
                campaign = Campaign.get_by_id(camp_id)
                return jsonify({"campaign": campaign})
                
            logger.debug("Fetching all campaigns")
            campaigns = Campaign.get_all()
            logger.debug(f"Found {len(campaigns) if campaigns else 0} campaigns")
            
            if not campaigns:
                logger.warning("No campaigns found in database")
                return jsonify({"campaigns": []})
                
            for campaign in campaigns:
                try:
                    campaign['ngay_bat_dau'] = campaign['ngay_bat_dau'].strftime('%d/%m/%Y') if campaign['ngay_bat_dau'] else None
                    campaign['ngay_ket_thuc'] = campaign['ngay_ket_thuc'].strftime('%d/%m/%Y') if campaign['ngay_ket_thuc'] else None
                except Exception as date_error:
                    logger.error(f"Error formatting dates for campaign {campaign.get('camp_id')}: {str(date_error)}")
                    
            logger.debug("Successfully processed all campaigns")
            return jsonify({"campaigns": campaigns})
        except Exception as e:
            logger.error(f"Error in get campaigns: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.json
            campaign_type_id = CampaignType.get_by_name(
                data['ten_loai_chien_dich'])
            if not campaign_type_id:
                return jsonify({"error": "Campaign type not found"}), 400

            # Chuẩn bị dữ liệu cho campaign
            campaign_data = {
                'ten_chien_dich': data['ten_chien_dich'],
                'camp_type_id': campaign_type_id,
                'ngan_sach_ngay': data.get('ngan_sach_ngay', 0),
                'tong_chi_phi': data.get('tong_chi_phi', 0),
                'ngay_bat_dau': datetime.strptime(data['ngay_bat_dau'], '%Y-%m-%d').strftime('%Y-%m-%d'),
                'ngay_ket_thuc': datetime.strptime(data['ngay_ket_thuc'], '%Y-%m-%d').strftime('%Y-%m-%d'),
                'campstatus_id': CampStatus.get_by_name('Đang chạy'),
                'customer_id': data.get('customer_id')
            }

            if data.get('source_id'):
                campaign_data['source_id'] = data.get('source_id')

            # Validate customer_id
            if not campaign_data['customer_id']:
                return jsonify({"error": "Customer ID is required"}), 400

            campaign = Campaign(**campaign_data)
            campaign_id = campaign.create()

            return jsonify({
                "message": "Campaign created successfully",
                "campaign_id": campaign_id
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, camp_id):
        try:
            data = request.json
            if 'ten_loai_chien_dich' in data:
                campaign_type_id = CampaignType.get_by_name(
                    data['ten_loai_chien_dich'])
                if not campaign_type_id:
                    return jsonify({"error": "Campaign type not found"}), 400
                data['camp_type_id'] = campaign_type_id
                del data['ten_loai_chien_dich']

            Campaign.update(camp_id, data)
            return jsonify({"message": "Campaign updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def delete(self, camp_id):
        try:
            Campaign.delete(camp_id)
            return jsonify({"message": "Campaign deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})
