from models.ads_group_product_group import AdsGroupProductGroup
from .auth.user import User
from .auth.role import Role
from .campaign.campaign import Campaign
from .campaign.campaign_type import CampaignType
from .campaign.campaign_status import CampaignStatus
from .campaign.ads import Ads
from .campaign.ads_format import AdsFormat
from .campaign.ads_group import AdsGroup
from .campaign.ads_group_status import AdsGroupStatus
from .campaign.ads_status import StatusAds
from .website.website import Website
from .website.website_status import WebsiteStatus
from .website.ads_zone import AdsZone
from .website.zone_price_setup import ZonePriceSetup
from .website.zone_price_mapping import ZonePriceMapping
from .website.global_price import GlobalPrice
from .website.price_type import PriceType
from .product import Product
from .product_status import ProductStatus
from .product import ProductGroup
from .product_group_mapping import ProductGroupMapping
from .publisher import Publisher
from .publisher_status import PublisherStatus
from .target_audience import TargetAudience
from .target_audience_status import TargetAudienceStatus
from .behaviour import Behaviour
from .ads_type import AdsType
from .ads_ecom import AdsEcom
from .ads_display import AdsDisplay
from .ads_native import AdsNative
from .ads_link_format import AdsLinkFormat
from .ad_size_format import AdSizeFormat
from .data_source import DataSource
from .source_status import SourceStatus
from .remarketing_setting import RemarketingSetting
from .remarketing_excluded_website import RemarketingExcludedWebsite
from .ads_group_product_selection import AdsGroupProductSelection
from .ads_group_target_audience import AdsGroupTargetAudience
from .ads_group_website import AdsGroupWebsite
from .website import AdsZoneSize
from .city import City
from .country import Country
from .customer import Customer
from .district import District

def create_all_tables():
    # Cấp độ 1 - Các bảng cơ sở
    Role.create_table()
    CampaignType.create_table()
    CampaignStatus.create_table()
    AdsGroupStatus.create_table()
    StatusAds.create_table()
    WebsiteStatus.create_table()
    ProductStatus.create_table()
    PublisherStatus.create_table()
    SourceStatus.create_table()
    AdsType.create_table()
    PriceType.create_table()
    Behaviour.create_table()
    Country.create_table()
    City.create_table()
    District.create_table()
    AdsZoneSize.create_table()
    TargetAudienceStatus.create_table()

    # Cấp độ 2 - Các bảng phụ thuộc đơn
    User.create_table()
    Publisher.create_table()
    Website.create_table()
    AdsFormat.create_table()
    DataSource.create_table()
    Campaign.create_table()
    Customer.create_table()
    Product.create_table()
    ProductGroup.create_table()
    TargetAudience.create_table()

    # Cấp độ 3 - Các bảng có nhiều phụ thuộc
    AdsGroup.create_table()
    Ads.create_table()
    AdsZone.create_table()
    ZonePriceSetup.create_table()
    GlobalPrice.create_table()
    ProductGroupMapping.create_table()

    # Cấp độ 4 - Các bảng ánh xạ và quan hệ
    AdsDisplay.create_table()
    AdsEcom.create_table()
    AdsNative.create_table()
    AdsGroupProductGroup.create_table()
    AdsGroupProductSelection.create_table()
    AdsGroupTargetAudience.create_table()
    AdsGroupWebsite.create_table()
    ZonePriceMapping.create_table()
    RemarketingSetting.create_table()
    RemarketingExcludedWebsite.create_table()
    AdSizeFormat.create_table()
    AdsLinkFormat.create_table()
