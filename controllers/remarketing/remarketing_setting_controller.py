from flask import request, jsonify
from models.remarketing_setting import RemarketingSetting
from models.remarketing_excluded_website import RemarketingExcludedWebsite
from controllers.base_controller import BaseController

class RemarketingSettingController(BaseController):
    def get(self, remarketing_id=None):
        try:
            if remarketing_id:
                remarketing = RemarketingSetting.get_by_id(remarketing_id)
                if not remarketing:
                    return jsonify({'message': 'Remarketing not found'}), 404
                
                # Get excluded websites
                excluded_websites = RemarketingExcludedWebsite.get_by_remarketing_id(remarketing_id)
                remarketing['excluded_websites'] = excluded_websites
                
                return jsonify(remarketing)
            else:
                remarketing_list = RemarketingSetting.get_all()
                return jsonify(remarketing_list)
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()
            
            # Create remarketing settings
            remarketing_data = {
                'tan_suat_hien_thi': data.get('display_frequency', 100),
                'thoi_gian_giua_2_lan': data.get('display_interval', 10),
                'thoi_gian_remarketing': data.get('remarketing_duration', 50),
                'dung_khi_click': data.get('stop_on_click', False),
                'dung_khi_du_luot_xem': data.get('stop_on_views', False),
                'so_luot_xem_toi_da': data.get('max_views', 1)
            }
            
            remarketing = RemarketingSetting(**remarketing_data)
            remarketing_id = remarketing.create()
            
            # Handle excluded websites if provided
            excluded_websites = data.get('excluded_websites', [])
            for website_id in excluded_websites:
                excluded = RemarketingExcludedWebsite(
                    remarketing_id=remarketing_id,
                    website_id=website_id
                )
                excluded.create()
                
            return jsonify({
                'message': 'Remarketing created successfully',
                'remarketing_id': remarketing_id
            })
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def put(self, remarketing_id):
        try:
            data = request.get_json()
            
            # Update remarketing settings
            remarketing_data = {
                'remarketing_id': remarketing_id,
                'tan_suat_hien_thi': data.get('display_frequency'),
                'thoi_gian_giua_2_lan': data.get('display_interval'),
                'thoi_gian_remarketing': data.get('remarketing_duration'),
                'dung_khi_click': data.get('stop_on_click'),
                'dung_khi_du_luot_xem': data.get('stop_on_views'),
                'so_luot_xem_toi_da': data.get('max_views')
            }
            
            remarketing = RemarketingSetting(**remarketing_data)
            remarketing.update()
            
            # Update excluded websites
            if 'excluded_websites' in data:
                # Remove existing exclusions
                RemarketingExcludedWebsite.delete_by_remarketing_id(remarketing_id)
                
                # Add new exclusions
                for website_id in data['excluded_websites']:
                    excluded = RemarketingExcludedWebsite(
                        remarketing_id=remarketing_id,
                        website_id=website_id
                    )
                    excluded.create()
            
            return jsonify({'message': 'Remarketing updated successfully'})
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def delete(self, remarketing_id):
        try:
            # This will cascade delete excluded websites due to foreign key constraint
            RemarketingSetting.delete(remarketing_id)
            return jsonify({'message': 'Remarketing deleted successfully'})
        except Exception as e:
            return jsonify({'message': str(e)}), 500 