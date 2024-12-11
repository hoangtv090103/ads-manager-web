# Auth
from .auth import Auth
from .role import Role 
from .user import User

# Trạng thái
from .campaign_status import CampStatus
from .ads_group_status import AdsGroupStatus
from .ads_status import StatusAds
from .website_status import WebsiteStatus
from .product_status import ProductStatus
from .publisher_status import PublisherStatus
from .source_status import SourceStatus
from .target_audience_status import TargetAudienceStatus
# from .ads_zone_status import AdsZoneStatus

# Cơ sở
from .behaviour import Behaviour
from .campaign_type import CampaignType
from .ads_type import AdsType
from .price_type import PriceType
from .country import Country
from .city import City
from .district import District
from .ads_zone_size import AdsZoneSize

# Thực thể chính
from .data_source import DataSource
from .campaign import Campaign
from .ads_format import AdsFormat
from .ads_group import AdsGroup
from .ads import Ads
from .website import Website
from .product import Product
from .product_group import ProductGroup
from .publisher import Publisher
from .target_audience import TargetAudience

# Bản đồ & Quan hệ
from .ads_display import AdsDisplay
from .ads_ecom import AdsEcom
from .ads_native import AdsNative
from .ads_link_format import AdsLinkFormat
from .ad_size_format import AdSizeFormat
from .ads_zone import AdsZone
from .zone_price_setup import ZonePriceSetup
from .zone_price_mapping import ZonePriceMapping
from .global_price import GlobalPrice
from .product_group_mapping import ProductGroupMapping
from .ads_group_product_group import AdsGroupProductGroup
# from .ads_group_product_selection import AdsGroupProductSelection
from .ads_group_target_audience import AdsGroupTargetAudience
from .ads_group_website import AdsGroupWebsite
from .remarketing_setting import RemarketingSetting
from .remarketing_excluded_website import RemarketingExcludedWebsite
from .publisher import Publisher
from .customer import Customer

def create_all_tables():
    # 1. Bảng Auth
    Role.create_table()
    User.create_table()
    
    # 2. Bảng Trạng thái
    Behaviour.create_table()
    CampStatus.create_table()
    AdsGroupStatus.create_table() 
    StatusAds.create_table()
    WebsiteStatus.create_table()
    ProductStatus.create_table()
    PublisherStatus.create_table()
    SourceStatus.create_table()
    TargetAudienceStatus.create_table()
    # AdsZoneStatus.create_table()

    # 3. Bảng Cơ sở
    User.create_table()
    CampaignType.create_table()
    AdsType.create_table()
    PriceType.create_table()
    Country.create_table()
    City.create_table()
    District.create_table()
    AdsZoneSize.create_table()

    # 4. Bảng Thực thể chính
    DataSource.create_table()
    Campaign.create_table()
    AdsFormat.create_table()
    AdsGroup.create_table()
    Ads.create_table()
    Publisher.create_table()
    Website.create_table()
    Product.create_table()
    TargetAudience.create_table()
    ProductGroup.create_table()
    Customer.create_table()

    # 5. Bảng Mappings & Quan hệ
    AdsDisplay.create_table()
    AdsEcom.create_table()
    AdsNative.create_table()
    AdsLinkFormat.create_table()
    AdSizeFormat.create_table()
    AdsZone.create_table()
    ZonePriceSetup.create_table()
    ZonePriceMapping.create_table()
    GlobalPrice.create_table()
    ProductGroupMapping.create_table()
    AdsGroupProductGroup.create_table()
    # AdsGroupProductSelection.create_table()
    AdsGroupTargetAudience.create_table()
    AdsGroupWebsite.create_table()
    RemarketingSetting.create_table()
    RemarketingExcludedWebsite.create_table()