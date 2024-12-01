from configs.db import get_db_connection


class WebsitePrice:
    def __init__(self, price_id=None, pub_id=None, website_id=None, 
                 pricetype_id=None, pricestatus_id=None, thoi_gian_ap_dung=None,
                 zone_id=None, zonestatus_id=None, adstype_id=None, 
                 format_id=None, gia_mua=0.0, gia_ban=0.0):
        self.price_id = price_id
        self.pub_id = pub_id
        self.website_id = website_id
        self.pricetype_id = pricetype_id
        self.pricestatus_id = pricestatus_id
        self.thoi_gian_ap_dung = thoi_gian_ap_dung
        self.zone_id = zone_id
        self.zonestatus_id = zonestatus_id
        self.adstype_id = adstype_id
        self.format_id = format_id
        self.gia_mua = gia_mua
        self.gia_ban = gia_ban

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS website_price (
                price_id SERIAL PRIMARY KEY,
                pub_id INTEGER,
                website_id INTEGER,
                pricetype_id INTEGER,
                pricestatus_id INTEGER,
                thoi_gian_ap_dung TIMESTAMP,
                zone_id INTEGER,
                zonestatus_id INTEGER,
                adstype_id INTEGER,
                format_id INTEGER,
                gia_mua DECIMAL(18,2),
                gia_ban DECIMAL(18,2),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (pub_id) REFERENCES publisher(publisher_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (zone_id) REFERENCES ads_zone(zone_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (pricetype_id) REFERENCES price_type(pricetype_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (pricestatus_id) REFERENCES price_status(pricestatus_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (zonestatus_id) REFERENCES ads_zone_status(zonestatus_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (adstype_id) REFERENCES ads_type(ads_type_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()
            
    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM website_price WHERE active = true')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
    @staticmethod
    def get_by_id(price_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM website_price WHERE price_id = %s', (price_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO website_price (pub_id, website_id, pricetype_id, pricestatus_id, thoi_gian_ap_dung, zone_id, zonestatus_id, adstype_id, format_id, gia_mua, gia_ban) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.pub_id, self.website_id, self.pricetype_id, self.pricestatus_id, self.thoi_gian_ap_dung, self.zone_id, self.zonestatus_id, self.adstype_id, self.format_id, self.gia_mua, self.gia_ban))
            conn.commit()


    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE website_price SET pub_id = ?, website_id = ?, pricetype_id = ?, pricestatus_id = ?, thoi_gian_ap_dung = ?, zone_id = ?, zonestatus_id = ?, adstype_id = ?, format_id = ?, gia_mua = ?, gia_ban = ? WHERE price_id = ?', (self.pub_id, self.website_id, self.pricetype_id, self.pricestatus_id, self.thoi_gian_ap_dung, self.zone_id, self.zonestatus_id, self.adstype_id, self.format_id, self.gia_mua, self.gia_ban, self.price_id))
            conn.commit()
            
    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE website_price SET active = false WHERE price_id = ?', (self.price_id,))
            conn.commit()
