from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from controllers.auth.auth_controller import LoginController, RegisterController
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

create_all_tables()
if __name__ == '__main__':
    app.run(debug=True)
