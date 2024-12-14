from flask import jsonify
from controllers.behaviour.behaviour_controller import BehaviourController
from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from flask_restful import Api
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from controllers.auth.auth_controller import LoginController, RegisterController, ForgotPasswordController, ResetPasswordController
from controllers.campaign.campaign_controller import CampaignController
from controllers.campaign.ads_group_controller import AdsGroupController
from controllers import *
from controllers.campaign.campaign_type_controller import CampaignTypeController
from controllers.website import *
from controllers.auth import *
from controllers.product import *
from controllers.target_audience import *
from controllers.account_controller import AccountController
from controllers.publisher.publisher_controller import PublisherController
from models import create_all_tables
from middlewares.auth_middleware import token_required
from controllers.report import WebsiteReportController
from controllers.report.publisher_report_controller import PublisherReportController
from controllers.report.zone_report_controller import ZoneReportController
from controllers.report.ad_format_report_controller import AdFormatReportController
from controllers.customer.customer_controller import CustomerController
from controllers.remarketing.remarketing_setting_controller import RemarketingController
from controllers.website.website_controller import WebsiteController
from controllers.ads_group.ads_group_controller import AdsGroupController
from controllers.ads_zone_size.ads_zone_size_controller import AdsZoneSizeController
from models.ads_format import AdsFormat
from controllers.price.price_controller import PriceController
from controllers.behaviour.behaviour_controller import BehaviourController
from controllers.auth.auth_controller import ForgotPasswordController

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

v1 = Blueprint('v1', __name__)
api = Api(v1)
app.register_blueprint(v1, url_prefix='/api/v1')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max-limit

# Campaign routes
api.add_resource(CampaignController,
                 '/campaigns',
                 '/campaigns/<int:camp_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Ads Group routes
api.add_resource(AdsGroupController,
                 '/ads-groups',
                 '/ads-groups/<int:ads_group_id>',
                 '/ads-groups/<int:ads_group_id>/product-groups',
                 '/ads-groups/<int:ads_group_id>/websites',
                 '/ads-groups/<int:ads_group_id>/product-groups/<int:product_group_id>',
                 '/ads-groups/<int:ads_group_id>/websites/<int:website_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# City routes
api.add_resource(CityController,
                 '/cities',
                 '/cities/<int:city_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Ads routes
api.add_resource(AdsController,
                 '/ads',
                 '/ads/<int:ads_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Website routes
api.add_resource(WebsiteController,
                 '/websites',
                 '/websites/<int:website_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Website Report routes
api.add_resource(WebsiteReportController,
                 '/websites/report',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Ads Zone routes
api.add_resource(AdsZoneController,
                 '/ads-zones',
                 '/ads-zones/<int:ads_zone_id>',
                 '/ads-zones/<int:ads_zone_id>/formats',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Website Price routes
api.add_resource(WebsitePriceController,
                 '/website-prices',
                 '/website-prices/<int:price_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Transaction routes
api.add_resource(TransactionController,
                 '/transactions',
                 '/transactions/<int:transaction_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Auth routes
api.add_resource(RegisterController,
                 '/auth/register', endpoint='register',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Login routes
api.add_resource(LoginController,
                 '/auth/login', endpoint='login'
                 )

# Forgot Password routes
api.add_resource(ForgotPasswordController,
                 '/auth/forgot-password', endpoint='forgot_password'
                 )

# Reset Password routes
api.add_resource(ResetPasswordController,
                 '/auth/reset-password', endpoint='reset_password'
                 )

# Role routes
api.add_resource(RoleController,
                 '/roles',
                 '/roles/<int:role_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Product routes
api.add_resource(ProductController,
                 '/products',
                 '/products/<int:product_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

api.add_resource(ProductImportController,
                 '/products/import',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Product Groups routes
api.add_resource(ProductGroupController,
                 '/product-groups',
                 '/product-groups/<int:group_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Data Sources routes
api.add_resource(DataSourceController,
                 '/data-sources',
                 '/data-sources/<int:source_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Target Audience routes
api.add_resource(TargetAudienceController,
                 '/target-audiences',
                 '/target-audiences/<int:ta_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )


# User routes
api.add_resource(AccountController,
                 '/accounts',
                 '/accounts/<int:user_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Publisher routes
api.add_resource(PublisherController,
                 '/publishers',
                 '/publishers/<int:publisher_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Publisher Report routes
api.add_resource(PublisherReportController,
                 '/publishers/report',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Zone Report routes
api.add_resource(ZoneReportController,
                 '/zones/report',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Ad Format Report routes
api.add_resource(AdFormatReportController,
                 '/ad-formats/report',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Campaign Type routes
api.add_resource(CampaignTypeController,
                 '/campaign-types',
                 '/campaign-types/<int:type_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Customer routes
api.add_resource(CustomerController,
                 '/customers',
                 '/customers/<int:customer_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Remarketing routes
api.add_resource(RemarketingController, '/api/remarketing',
                 '/api/remarketing/<int:remarketing_id>')

# Ads Zone Size routes
api.add_resource(AdsZoneSizeController,
                 '/ads-zone-sizes',
                 '/ads-zone-sizes/<int:size_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Price routes
api.add_resource(PriceController,
                 '/prices',
                 '/prices/<int:price_id>',
                 resource_class_kwargs={'decorators': [token_required]}
                 )

# Add behaviour routes
api.add_resource(BehaviourController,
                 '/behaviours',
                 '/behaviours/<int:behav_id>',
                 resource_class_kwargs={'decorators': [token_required]})


@app.route('/api/v1/ad-size-formats/<int:size_id>', methods=['GET'])
def get_ad_formats_by_size(size_id):
    try:
        formats = AdsFormat.get_by_size_id(size_id)
        if not formats:
            # Trả về mảng rỗng thay vì null
            return jsonify({'success': True, 'formats': []})
        return jsonify({'success': True, 'formats': formats})
    except Exception as e:
        print(f"Error getting formats: {str(e)}")  # Log lỗi để debug
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/v1/prices/formats', methods=['GET'])
def get_formats_for_pricing():
    return PriceController().get_formats_for_pricing()


create_all_tables()
if __name__ == '__main__':
    app.run(debug=True)
