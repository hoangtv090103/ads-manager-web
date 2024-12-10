from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from controllers.auth.auth_controller import LoginController, RegisterController
from controllers.campaign.campaign_controller import CampaignController
from controllers.campaign.ads_group_controller import AdsGroupController
from controllers import *
from controllers.website import *
from controllers.auth import *
from controllers.product import *
from controllers.target_audience import *
from controllers.user_controller import AccountController
from models import create_all_tables

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

v1 = Blueprint('v1', __name__)
api = Api(v1)
@v1.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

app.register_blueprint(v1, url_prefix='/api/v1')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max-limit

# Campaign routes
api.add_resource(CampaignController,
                 '/campaigns',
                 '/campaigns/<int:camp_id>'
                 )

# Ads Group routes
api.add_resource(AdsGroupController,
                 '/ads-groups',
                 '/ads-groups/<int:ads_group_id>'
                 )

# City routes
api.add_resource(CityController,
                 '/cities',
                 '/cities/<int:city_id>'
                 )

# Ads routes
api.add_resource(AdsController,
                 '/ads',
                 '/ads/<int:ads_id>'
                 )

# Website routes
api.add_resource(WebsiteController,
                 '/websites',
                 '/websites/<int:website_id>'
                 )

# Ads Zone routes
api.add_resource(AdsZoneController,
                 '/ads-zones',
                 '/ads-zones/<int:ads_zone_id>'
                 )

# Website Price routes
api.add_resource(WebsitePriceController,
                 '/website-prices',
                 '/website-prices/<int:price_id>'
                 )

# Transaction routes
api.add_resource(TransactionController,
                 '/transactions',
                 '/transactions/<int:transaction_id>'
                 )

# Auth routes
api.add_resource(RegisterController,
                 '/auth/register', endpoint='register', methods=['POST'],
                 )

# Login routes
api.add_resource(LoginController,
                 '/auth/login', endpoint='login', methods=['POST'],
                 )

# Role routes
api.add_resource(RoleController,
                 '/roles',
                 '/roles/<int:role_id>'
                 )

# Product routes
api.add_resource(ProductController,
                 '/products',
                 '/products/<int:product_id>'
                 )
api.add_resource(ProductImportController, '/products/import')

# Product Groups routes
api.add_resource(ProductGroupController,
                 '/product-groups',
                 '/product-groups/<int:group_id>'
                 )

# Data Sources routes
api.add_resource(DataSourceController,
                 '/data-sources',
                 '/data-sources/<int:source_id>'
                 )

# Target Audience routes
api.add_resource(TargetAudienceController,
                 '/target-audiences',
                 '/target-audiences/<int:ta_id>'
                 )

# Target Audience Status routes
api.add_resource(TargetAudienceStatusController,
                 '/target-audience-statuses',
                 '/target-audience-statuses/<int:status_id>'
                 )


# User routes
api.add_resource(AccountController,
                 '/accounts',
                 '/accounts/<int:user_id>'
                 )


create_all_tables()
if __name__ == '__main__':
    app.run(debug=True)
