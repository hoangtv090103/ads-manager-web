from flask import request, jsonify
from models.ads_group_product_group import AdsGroupProductGroup
from models.ads_group_product_selection import AdsGroupProductSelection
from models.ads_group_website import AdsGroupWebsite
from controllers.base_controller import BaseController

class AdsGroupController(BaseController):
    def get_product_groups(self, ads_group_id):
        try:
            product_groups = AdsGroupProductGroup.get_by_ads_group_id(ads_group_id)
            return jsonify(product_groups)
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def add_product_groups(self, ads_group_id):
        try:
            data = request.get_json()
            product_group_ids = data.get('product_group_ids', [])
            selection_type = data.get('selection_type')
            
            # Create product selection record
            selection = AdsGroupProductSelection(
                ads_group_id=ads_group_id,
                selection_type=selection_type
            )
            selection.create()
            
            # Add product groups
            results = []
            for product_group_id in product_group_ids:
                group = AdsGroupProductGroup(
                    ads_group_id=ads_group_id,
                    product_group_id=product_group_id
                )
                group_id = group.create()
                results.append(group_id)
                
            return jsonify({
                'message': 'Product groups added successfully',
                'group_ids': results
            })
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def get_websites(self, ads_group_id):
        try:
            websites = AdsGroupWebsite.get_by_ads_group_id(ads_group_id)
            return jsonify(websites)
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def add_websites(self, ads_group_id):
        try:
            data = request.get_json()
            website_ids = data.get('website_ids', [])
            
            results = []
            for website_id in website_ids:
                website = AdsGroupWebsite(
                    ads_group_id=ads_group_id,
                    website_id=website_id
                )
                website_id = website.create()
                results.append(website_id)
                
            return jsonify({
                'message': 'Websites added successfully',
                'website_ids': results
            })
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def remove_website(self, ads_group_id, website_id):
        try:
            AdsGroupWebsite.delete(website_id)
            return jsonify({'message': 'Website removed successfully'})
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def remove_product_group(self, ads_group_id, product_group_id):
        try:
            AdsGroupProductGroup.delete(ads_group_id, product_group_id)
            return jsonify({'message': 'Product group removed successfully'})
        except Exception as e:
            return jsonify({'message': str(e)}), 500 