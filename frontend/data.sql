DROP TABLE IF EXISTS ads_format CASCADE;
DROP TABLE IF EXISTS ad_size_format CASCADE;
DROP TABLE IF EXISTS price_type CASCADE;
DROP TABLE IF EXISTS source_status CASCADE;
DROP TABLE IF EXISTS product_status CASCADE;
DROP TABLE IF EXISTS ads_group_status CASCADE;
DROP TABLE IF EXISTS campaign_type CASCADE;


INSERT INTO
    ads_zone_size (ten_kich_thuoc)
VALUES ('375x400 - In page'),
    ('300x600 - In page'),
    ('375x600 - In page'),
    ('300x250 - In page'),
    ('375x810 - In page'),
    ('359x70 - Top banner'),
    ('640x320 - Top banner'),
    ('375x180 - Top banner'),
    ('375x810 - Popup mobile'),
    ('375x120 - In footer'),
    ('320x100 - In footer'),
    ('160x600 - Side page');

-- Native Ads formats
INSERT INTO
    ads_format (campaign_type_id, format_name)
SELECT ct.camp_type_id, format_name
FROM (
        VALUES ('Native video post'), ('Native post in read')
    ) AS formats (format_name)
    CROSS JOIN campaign_type ct
WHERE
    ct.ten_loai_chien_dich = 'Native Ads';

-- Display Ads formats
INSERT INTO
    ads_format (campaign_type_id, format_name)
SELECT ct.camp_type_id, format_name
FROM (
        VALUES ('Notification Banner'), ('CatFish Collab Branding'), ('Popup Banner Branding'), ('CatFish Collab Video'), ('Popup Banner Video'), (
                'Interscroller Video Branding'
            ), ('CatFish Graphic Banner'), ('In Read Branding'), ('Banner Medium 300x250'), ('Banner Standard 640x320'), ('Banner Standard 160x600'), ('Text Ads 300x600'), ('Text Ads 300x250'), ('Text Ads 320x100')
    ) AS formats (format_name)
    CROSS JOIN campaign_type ct
WHERE
    ct.ten_loai_chien_dich = 'Display Ads';

-- Ecommerce formats
INSERT INTO
    ads_format (campaign_type_id, format_name)
SELECT ct.camp_type_id, format_name
FROM (
        VALUES ('Mobile Banner Card'), ('Interactive Banner'), ('Flying Carpet'), ('In Read Ecommerce'), ('Post In Read'), ('CatFish Ecom'), ('CatFish Video Ecom')
    ) AS formats (format_name)
    CROSS JOIN campaign_type ct
WHERE
    ct.ten_loai_chien_dich = 'Ecommerce';

INSERT INTO
    ad_size_format (format_id, size_id)
SELECT f.format_id, s.size_id
FROM ads_format f
    CROSS JOIN ads_zone_size s
WHERE (
        f.format_name = 'Native video post'
        AND s.ten_kich_thuoc = '375x400 - In page'
    )
    OR (
        f.format_name = 'Native post in read'
        AND s.ten_kich_thuoc = '375x400 - In page'
    )
    OR (
        f.format_name = 'Notification Banner'
        AND s.ten_kich_thuoc = '359x70 - Top banner'
    )
    OR (
        f.format_name = 'CatFish Collab Branding'
        AND s.ten_kich_thuoc = '375x120 - In footer'
    )
    OR (
        f.format_name = 'Popup Banner Branding'
        AND s.ten_kich_thuoc = '375x810 - Popup mobile'
    )
    OR (
        f.format_name = 'CatFish Collab Video'
        AND s.ten_kich_thuoc = '375x120 - In footer'
    )
    OR (
        f.format_name = 'Popup Banner Video'
        AND s.ten_kich_thuoc = '375x810 - Popup mobile'
    )
    OR (
        f.format_name = 'Interscroller Video Branding'
        AND s.ten_kich_thuoc = '300x600 - In page'
    )
    OR (
        f.format_name = 'CatFish Graphic Banner'
        AND s.ten_kich_thuoc = '320x100 - In footer'
    )
    OR (
        f.format_name = 'In Read Branding'
        AND s.ten_kich_thuoc = '375x600 - In page'
    )
    OR (
        f.format_name = 'Banner Medium 300x250'
        AND s.ten_kich_thuoc = '300x250 - In page'
    )
    OR (
        f.format_name = 'Banner Standard 640x320'
        AND s.ten_kich_thuoc = '640x320 - Top banner'
    )
    OR (
        f.format_name = 'Banner Standard 160x600'
        AND s.ten_kich_thuoc = '160x600 - Side page'
    )
    OR (
        f.format_name = 'Text Ads 300x600'
        AND s.ten_kich_thuoc = '300x600 - In page'
    )
    OR (
        f.format_name = 'Text Ads 300x250'
        AND s.ten_kich_thuoc = '300x250 - In page'
    )
    OR (
        f.format_name = 'Text Ads 320x100'
        AND s.ten_kich_thuoc = '320x100 - In footer'
    )
    OR (
        f.format_name = 'Mobile Banner Card'
        AND s.ten_kich_thuoc = '375x180 - Top banner'
    )
    OR (
        f.format_name = 'Interactive Banner'
        AND s.ten_kich_thuoc = '375x810 - Popup mobile'
    )
    OR (
        f.format_name = 'Flying Carpet'
        AND s.ten_kich_thuoc = '375x810 - In page'
    )
    OR (
        f.format_name = 'In Read Ecommerce'
        AND s.ten_kich_thuoc = '375x600 - In page'
    )
    OR (
        f.format_name = 'Post In Read'
        AND s.ten_kich_thuoc = '375x600 - In page'
    )
    OR (
        f.format_name = 'CatFish Ecom'
        AND s.ten_kich_thuoc = '375x120 - In footer'
    )
    OR (
        f.format_name = 'CatFish Video Ecom'
        AND s.ten_kich_thuoc = '375x120 - In footer'
    );

INSERT INTO
    price_type (price_type_name)
VALUES ('CPM'),
    ('CPC');

INSERT INTO
    source_status (ten_trang_thai)
VALUES ('Đang chờ xử lý'),
    ('Đang xử lý'),
    ('Đã xử lý'),
    ('Lỗi');

INSERT INTO
    product_status (ten_trang_thai)
VALUES ('Thực chạy'),
    ('Hết hàng'),
    ('Đã tắt');
