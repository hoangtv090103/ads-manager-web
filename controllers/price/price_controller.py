from flask import request, jsonify
from controllers.base_controller import BaseController
from models.ads_zone_format import AdsZoneFormat
from models.global_price import GlobalPrice
from models.price_type import PriceType
from models.website import Website
from models.zone_price_setup import ZonePriceSetup
from models.zone_price_mapping import ZonePriceMapping
from models.ads_zone import AdsZone
from models.ads_format import AdsFormat
from datetime import datetime, date
from models.campaign_type import CampaignType
from models.ad_size_format import AdSizeFormat
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class PriceController(BaseController):
    def get(self, price_id=None):
        params = request.args
        view_type = params.get('view_type', 'website')  # 'website' or 'zone'
        website_id = params.get('website_id')

        try:
            if view_type == 'website':
                response = self._get_global_prices(price_id, website_id)
            else:
                response = self._get_zone_prices(price_id, website_id)

            return response
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })

    def _get_global_prices(self, price_id=None, website_id=None):
        try:
            if price_id:
                price = GlobalPrice.get_by_id(price_id)
                if not price:
                    return jsonify({
                        'success': False,
                        'message': 'Không tìm thấy bảng giá'
                    })
                return jsonify({
                    'success': True,
                    'data': price
                })
            else:
                if website_id:
                    prices = GlobalPrice.get_by_website_id(website_id)
                else:
                    prices = GlobalPrice.get_all()

                # Get all formats and campaign types for column headers
                formats_data = self.get_formats_for_pricing()

                return jsonify({
                    'success': True,
                    'prices': prices,
                    'formats': formats_data.json['data']['formats_by_type']
                })
        except Exception as e:
            raise e

    def _get_zone_prices(self, price_id=None, website_id=None):
        try:
            if price_id:
                price = ZonePriceSetup.get_by_id(price_id)
                if not price:
                    return jsonify({
                        'success': False,
                        'message': 'Không tìm thấy bảng giá'
                    })
                return jsonify({
                    'success': True,
                    'data': price
                })
            else:
                # Get zone price setups with all related data
                price_data = ZonePriceSetup.get_all(website_id)

                # If no data found, return empty response
                if not price_data:
                    return jsonify({
                        'success': True,
                        'prices': {},
                        'formats': {}
                    })
                    
                # Return the grouped data directly
                return jsonify({
                    'success': True,
                    'formats': price_data['formats'],
                    'prices': price_data['zone_prices']
                })

        except Exception as e:
            raise e

    def _get_zone_formats(self, zone_id):
        """Get all formats available for a specific zone"""
        try:
            # Get zone size
            zone = AdsZone.get_by_id(zone_id)
            if not zone:
                return []

            # Get formats for this size
            size_formats = AdSizeFormat.get_by_size_id(zone['size_id'])

            # Group formats by campaign type
            formats_by_type = {}
            for format in size_formats:
                camp_type = format['ten_loai_chien_dich']
                if camp_type not in formats_by_type:
                    formats_by_type[camp_type] = []
                formats_by_type[camp_type].append({
                    'format_id': format['format_id'],
                    'format_name': format['format_name']
                })

            return formats_by_type
        except Exception as e:
            print(f"Error getting zone formats: {str(e)}")
            return []

    def get_zone_formats(self, zone_id):
        """API endpoint to get formats for a specific zone"""
        try:
            formats = self._get_zone_formats(zone_id)
            return jsonify({
                'success': True,
                'data': formats
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })

    def post(self):
        try:
            data = request.get_json()
            website_id = data.get('website_id')
            price_type = data.get('type')  # 'uniform' or 'zone'
            start_date = data.get('start_date')
            prices = data.get('prices', [])

            if not website_id or not price_type or not start_date or not prices:
                return jsonify({
                    'success': False,
                    'message': 'Thiếu thông tin bắt buộc'
                })

            # Verify website exists
            website = Website.get_by_id(website_id)
            if not website:
                return jsonify({
                    'success': False,
                    'message': 'Website không tồn tại'
                })

            if price_type == 'uniform':
                return self._create_uniform_prices(website_id, start_date, prices)
            else:
                return self._create_individual_prices(website_id, start_date, prices)

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })

    def _create_uniform_prices(self, website_id, start_date, prices):
        try:
            cpm_type = PriceType.get_by_name('CPM')
            cpc_type = PriceType.get_by_name('CPC')

            if not cpm_type or not cpc_type:
                raise Exception("Price types not found")

            # Get all formats to map names to IDs
            all_formats = AdsFormat.get_all()
            format_map = {format['format_name']: format['format_id']
                          for format in all_formats}

            # Tạo global price setup cho mỗi format
            created_prices = []
            for price in prices:
                format_name = price.get('format_name')
                format_id = format_map.get(format_name)

                if not format_id:
                    continue  # Skip if format not found

                buy_type = price.get('buy_type')
                sell_type = price.get('sell_type')

                # Create global price record
                global_price = GlobalPrice(
                    website_id=website_id,
                    is_uniform_price=True,
                    format_id=format_id,
                    buy_price=price.get('buy_price', 0),
                    sell_price=price.get('sell_price', 0),
                    buy_price_unit_id=cpm_type['price_type_id'] if buy_type == 'CPM' else cpc_type['price_type_id'],
                    sell_price_unit_id=cpm_type['price_type_id'] if sell_type == 'CPM' else cpc_type['price_type_id'],
                    start_date=start_date
                )
                price_id = global_price.save()
                created_prices.append(price_id)

            if not created_prices:
                raise Exception("Không tìm thấy định dạng hợp lệ để tạo giá")

            return jsonify({
                'success': True,
                'message': 'Tạo bảng giá chung thành công',
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })

    def _create_individual_prices(self, website_id, start_date, prices):
        try:
            # Lấy price type IDs từ bảng price_type
            cpm_type = PriceType.get_by_name('CPM')
            cpc_type = PriceType.get_by_name('CPC')

            if not cpm_type or not cpc_type:
                raise Exception("Price types not found")

            # Group prices by zone_id
            zone_prices = {}
            for price in prices:
                zone_id = price.get('zone_id')
                if zone_id not in zone_prices:
                    zone_prices[zone_id] = []
                zone_prices[zone_id].append(price)

            # Xử lý từng zone
            created_setups = []
            for zone_id, zone_price_list in zone_prices.items():
                # Verify zone exists
                zone = AdsZone.get_by_id(zone_id)
                if not zone:
                    raise Exception(f"Zone {zone_id} not found")

                # Verify zone belongs to website
                if zone['website_id'] != website_id:
                    raise Exception(
                        f"Zone {zone_id} does not belong to website {website_id}")

                # Tạo zone price setup cho mỗi zone
                for price in zone_price_list:
                    buy_type = price.get('buy_type')
                    sell_type = price.get('sell_type')
                    format_id = price.get('format_id')

                    # Verify format exists and is associated with zone
                    zone_formats = AdsZoneFormat.get_by_zone_id(zone_id)
                    if not any(zf['format_id'] == format_id for zf in zone_formats):
                        raise Exception(
                            f"Format {format_id} is not associated with zone {zone_id}")

                    # Tạo zone price setup
                    setup = ZonePriceSetup(
                        website_id=website_id,
                        buy_price=price.get('buy_price', 0),
                        buy_price_type_id=cpm_type['price_type_id'] if buy_type == 'CPM' else cpc_type['price_type_id'],
                        sell_price=price.get('sell_price', 0),
                        sell_price_type_id=cpm_type['price_type_id'] if sell_type == 'CPM' else cpc_type['price_type_id'],
                        start_date=start_date
                    )
                    setup_id = setup.save()
                    created_setups.append(setup_id)

                    # Tạo mapping giữa zone và price setup
                    mapping = ZonePriceMapping(
                        zone_price_setup_id=setup_id,
                        zone_id=zone_id
                    )
                    mapping.create()

            return {
                'success': True,
                'message': 'Tạo bảng giá riêng thành công',
                'setup_ids': created_setups
            }, 201

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500

    def put(self, price_id):
        try:
            data = request.get_json()
            price_type = data.get('type', 'uniform')

            if price_type == 'uniform':
                # Update global price
                price = GlobalPrice.get_by_id(price_id)
                if not price:
                    return {
                        'success': False,
                        'message': 'Không tìm thấy bảng giá'
                    }, 404

                # Update price
                global_price = GlobalPrice(**data)
                global_price.global_price_id = price_id
                global_price.update()
            else:
                # Update zone price setup
                setup = ZonePriceSetup.get_by_id(price_id)
                if not setup:
                    return {
                        'success': False,
                        'message': 'Không tìm thấy bảng giá'
                    }, 404

                setup_obj = ZonePriceSetup(**data)
                setup_obj.zone_price_setup_id = price_id
                setup_obj.update()

            return {
                'success': True,
                'message': 'Cập nhật bảng giá thành công'
            }

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500

    def delete(self, price_id):
        try:
            data = request.get_json()
            price_type = data.get('type', 'uniform')

            if price_type == 'uniform':
                GlobalPrice.delete_by_id(price_id)
            else:
                ZonePriceSetup.delete_by_id(price_id)

            return {
                'success': True,
                'message': 'Xóa bảng giá thành công'
            }

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500

    def get_price_type(self, price_type_name):
        price_type = PriceType.get_by_name(price_type_name)
        return price_type

    def get_formats(self):
        try:
            # Get all campaign types
            campaign_types = CampaignType.get_all()

            # Get all formats
            formats = AdsFormat.get_all()

            # Group formats by campaign type
            formats_with_type = []
            for format in formats:
                # Find campaign type info
                campaign_type = next(
                    (ct for ct in campaign_types if ct['camp_type_id']
                     == format['campaign_type_id']),
                    None
                )
                if campaign_type:
                    formats_with_type.append({
                        **format,
                        'ten_loai_chien_dich': campaign_type['ten_loai_chien_dich']
                    })

            return {
                'success': True,
                'formats': formats_with_type
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500

    def get_formats_for_pricing(self):
        """Get all formats grouped by campaign type for pricing table"""
        try:
            # Get all campaign types
            campaign_types = CampaignType.get_all()
            if not campaign_types:
                return {
                    'success': False,
                    'message': 'Không tìm thấy loại chiến dịch'
                }, 404

            # Get all formats with campaign type info
            formats_by_type = {}
            for campaign_type in campaign_types:
                formats = AdsFormat.get_all()
                campaign_formats = []

                for format in formats:
                    if format['campaign_type_id'] == campaign_type['camp_type_id']:
                        campaign_formats.append({
                            'format_id': format['format_id'],
                            'format_name': format['format_name'],
                            'campaign_type_id': format['campaign_type_id']
                        })

                if campaign_formats:  # Only add if there are formats for this type
                    formats_by_type[campaign_type['ten_loai_chien_dich']
                                    ] = campaign_formats

            # Get price types for dropdowns
            price_types = PriceType.get_all()

            return jsonify({
                'success': True,
                'data': {
                    'formats_by_type': formats_by_type,
                    'price_types': price_types
                }
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })
