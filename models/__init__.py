from .campaign.status_ads import StatusAds
from .campaign.ads import Ads
from .campaign.ads_format import AdsFormat
from .campaign import AdsGroup, Campaign
from .campaign.ads_group_status import AdsGroupStatus
from .ads_type import AdsType
from .age_target import AgeTarget
from .city import City
from .country import Country
from .customer import Customer
from .district import District
from .geo_target import GeoTarget
from .geogroup_target import GeoGroupTarget
from .gioitinh_target import GioiTinhTarget
from .website.price_status import PriceStatus
from .website.price_type import PriceType
from .product import Product, ProductGroup, ProductStatus
from .publisher import Publisher
from .publisher_status import PublisherStatus
from .target_audience import TargetAudience
from .target_audience_status import TargetAudienceStatus
from .transaction import TransactionSystem
from .typemarketing_target import TypeRemarketingTarget
from .auth.role import Role
from .website import AdsZone, AdsZoneStatus, AdsZoneSize, DataSource, DataSourceStatus, Website, WebsiteStatus, WebsitePrice
from .user import *

# Level 1 - Base tables (no foreign keys)
ProductStatus.create_table()
PublisherStatus.create_table()
WebsiteStatus.create_table()
AdsGroupStatus.create_table()
TargetAudienceStatus.create_table()  # Needed before TargetAudience
PriceStatus.create_table()
PriceType.create_table()
AdsType.create_table()
AdsFormat.create_table()
AdsZoneSize.create_table()
GioiTinhTarget.create_table()
AgeTarget.create_table()
GeoGroupTarget.create_table()
TypeRemarketingTarget.create_table()
StatusAds.create_table()
Role.create_table()
DataSourceStatus.create_table()

# Level 2 - Tables with single dependencies
Country.create_table()
City.create_table()  # Depends on Country
District.create_table()  # Depends on City
Publisher.create_table()  # Depends on PublisherStatus
GeoTarget.create_table()  # Depends on GeoGroupTarget
User.create_table()  # Depends on Role

# Level 3 - Tables with multiple dependencies
Website.create_table()  # Depends on Publisher, WebsiteStatus
AdsZone.create_table()  # Depends on Website, AdsZoneSize
AdsZoneStatus.create_table()  # Depends on AdsZone
Customer.create_table()  # Depends on Country, City, District
TargetAudience.create_table()  # Depends on TargetAudienceStatus
Product.create_table()  # Depends on ProductStatus and Customer
ProductGroup.create_table()  # Depends on Product
DataSource.create_table()  # Depends on DataSourceStatus and User

# Level 4 - Complex relationships
Campaign.create_table()  # Depends on Customer, AdsType
AdsGroup.create_table()  # Depends on Campaign, AdsGroupStatus, etc
Ads.create_table()  # Depends on AdsGroup, StatusAds
TransactionSystem.create_table()  # Depends on Customer
WebsitePrice.create_table()  # Depends on multiple tables
