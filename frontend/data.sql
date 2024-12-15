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


INSERT INTO public.ads (
    ads_id,
    ads_group_id,
    ten_tin_quang_cao,
    url_dich,
    tong_chi_phi,
    luot_xem,
    luot_nhan,
    ctr,
    cpc,
    cpm,
    so_luong_mua_hang,
    conversion_rate,
    cps,
    video_watches_at_3s,
    video_watches_at_25,
    video_watches_at_50,
    video_watches_at_75,
    video_watches_at_100,
    created_at,
    updated_at,
    active
) VALUES
    (1, 4,  'Khuyến mãi Tết - Mua 1 Tặng 1', 'https://example.com/tet-sale', 2000000, 10000, 500, 5.0, 4000, 20000, 20, 4.0, 100000, 300, 200, 150, 100, 50, '2022-01-01 00:00:00', '2022-01-01 00:00:00', TRUE),
    (2, 4,  'Giảm giá cuối tuần - Đến 50%', 'https://example.com/weekend-sale', 5000000, 20000, 1000, 5.0, 5000, 25000, 50, 5.0, 100000, 500, 400, 350, 300, 200, '2022-01-08 00:00:00', '2022-01-08 00:00:00', TRUE),
    (3, 5,  'Ra mắt sản phẩm mới - Miễn phí vận chuyển', 'https://example.com/new-product', 1500000, 7000, 350, 5.0, 4285.71, 21428.57, 10, 2.0, 150000, 200, 150, 100, 80, 50, '2022-01-15 00:00:00', '2022-01-15 00:00:00', TRUE),
    (4, 5, 'Flash Sale 12h - Hàng ngàn sản phẩm giảm giá', 'https://example.com/flash-sale', 8000000, 40000, 2000, 5.0, 4000, 20000, 80, 4.0, 100000, 800, 600, 500, 400, 300, '2022-01-22 00:00:00', '2022-01-22 00:00:00', TRUE),
    (5, 6,  'Voucher giảm 100k cho đơn từ 500k', 'https://example.com/voucher-100k', 3000000, 15000, 750, 5.0, 4000, 20000, 30, 2.0, 100000, 300, 250, 200, 150, 100, '2022-01-29 00:00:00', '2022-01-29 00:00:00', TRUE),
    (6, 4,  'Săn Deal Hot - Giá sốc từ 9k', 'https://example.com/deal-hot', 6000000, 25000, 1200, 4.8, 5000, 24000, 60, 2.4, 100000, 700, 500, 400, 300, 200, '2022-02-05 00:00:00', '2022-02-05 00:00:00', TRUE),
    (7, 6,  'Đồng giá toàn sàn 99k', 'https://example.com/99k-sale', 4000000, 18000, 900, 5.0, 4444.44, 22222.22, 40, 2.2, 100000, 400, 300, 250, 200, 150, '2022-02-12 00:00:00', '2022-02-12 00:00:00', TRUE),
    (8, 6,  'Deal HOT cho tín đồ công nghệ', 'https://example.com/tech-deal', 7000000, 35000, 1800, 5.1, 3888.89, 20000, 70, 2.0, 100000, 900, 700, 600, 500, 400, '2022-02-19 00:00:00', '2022-02-19 00:00:00', TRUE),
    (9, 4,  'Quà tặng đặc biệt cho khách hàng VIP', 'https://example.com/vip-gift', 9000000, 45000, 2300, 5.1, 3913.04, 20000, 90, 2.0, 100000, 1000, 800, 700, 600, 500, '2022-02-26 00:00:00', '2022-02-26 00:00:00', TRUE),
    (10, 5,  'Sale cuối tháng - Giảm thêm 10% cho tất cả sản phẩm', 'https://example.com/month-end-sale', 11000000, 50000, 2500, 5.0, 4400, 22000, 100, 2.0, 100000, 1200, 1000, 800, 700, 600, '2022-03-01 00:00:00', '2022-03-01 00:00:00', TRUE);