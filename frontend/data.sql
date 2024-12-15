-- Thêm roles

-- Thêm users (password hash cho "123456")
INSERT INTO users (user_id, username, email, password, role_id, active) VALUES
-- Admin users
(1, 'admin', 'Administrator', 'admin@novanet.vn', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 1, true)

-- Publisher users
(2, 'vietnamnet', 'VietNamNet', 'publisher@vietnamnet.vn', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 2, true),
(3, 'dantri', 'Dân Trí', 'publisher@dantri.vn', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 2, true),
(4, 'vnexpress', 'VnExpress', 'publisher@vnexpress.net', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 2, true),

-- Customer users
(5, 'tgdd', 'Thế Giới Di Động', 'marketing@thegioididong.com', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 2, true),
(6, 'fpt', 'FPT Shop', 'marketing@fptshop.com.vn', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 2, true),
(7, 'shopee', 'Shopee', 'marketing@shopee.vn', '$2b$12$LQVGHl9.8vQVBB6v9X8/suYY3t/wPyUTESVFyBCH6.GGk9GNhYwQe', 2, true);

-- Thêm publishers
INSERT INTO publisher (publisher_id, ten_publisher, user_id, email, so_dien_thoai, active) VALUES
(1, 'VietNamNet', 2, 'publisher@vietnamnet.vn', '0987654321', true),
(2, 'Dân Trí', 3, 'publisher@dantri.vn', '0987654322', true),
(3, 'VnExpress', 4, 'publisher@vnexpress.net', '0987654323', true);

-- Thêm customers
INSERT INTO customer (
    customer_id, 
    ho_va_ten, 
    user_id,
    gioi_tinh,
    ten_doanh_nghiep,
    dia_chi_doanh_nghiep,
    website_doanh_nghiep,
    so_dien_thoai,
    email_doanh_nghiep,
    ma_remarketing,
    active
) VALUES
(1, 'Thế Giới Di Động', 5, 1, 'Công ty CP Thế Giới Di Động', 
   '128 Trần Quang Khải, P. Tân Định, Q.1, TP.HCM', 
   'www.thegioididong.com', 
   '0987654324',
   'marketing@thegioididong.com',
   'GTM-TGDD123',
   true),

(2, 'FPT Shop', 6, 1, 'Công ty CP Bán lẻ Kỹ thuật số FPT', 
   'Tòa nhà FPT Cầu Giấy, Số 17 Duy Tân, Cầu Giấy, Hà Nội',
   'www.fptshop.com.vn',
   '0987654325',
   'marketing@fptshop.com.vn',
   'GTM-FPT123',
   true),

(3, 'Shopee', 7, 1, 'Công ty TNHH Shopee', 
   'Tòa nhà Lim Tower, 9-11 Tôn Đức Thắng, Bến Nghé, Q.1, TP.HCM',
   'www.shopee.vn',
   '0987654326',
   'marketing@shopee.vn',
   'GTM-SHOPEE123',
   true);

-- Reset sequence
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));
SELECT setval('publisher_publisher_id_seq', (SELECT MAX(publisher_id) FROM publisher));
SELECT setval('customer_customer_id_seq', (SELECT MAX(customer_id) FROM customer));
