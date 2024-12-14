from configs.db import get_db_connection
from decimal import Decimal
from datetime import datetime, date

def format_value(value):
    """Format values for JSON serialization"""
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    return value

class ZonePriceSetup:
    def __init__(self, zone_price_setup_id=None, website_id=None,
                 buy_price=0.0, buy_price_type_id=None,
                 sell_price=0.0, sell_price_type_id=None,
                 start_date=None, created_at=None, updated_at=None,
                 active=True):
        self.zone_price_setup_id = zone_price_setup_id
        self.website_id = website_id
        self.buy_price = buy_price
        self.buy_price_type_id = buy_price_type_id
        self.sell_price = sell_price
        self.sell_price_type_id = sell_price_type_id
        self.start_date = start_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.active = active

    @staticmethod
    def _format_row(row_dict):
        """Format a row dictionary for JSON serialization"""
        return {key: format_value(value) for key, value in row_dict.items()}

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS zone_price_setup (
                zone_price_setup_id SERIAL PRIMARY KEY,
                website_id INTEGER NOT NULL,
                buy_price DECIMAL(15,2) NOT NULL,
                buy_price_type_id INTEGER NOT NULL,
                sell_price DECIMAL(15,2) NOT NULL,
                sell_price_type_id INTEGER NOT NULL,
                start_date TIMESTAMPTZ NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (buy_price_type_id) REFERENCES price_type(price_type_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (sell_price_type_id) REFERENCES price_type(price_type_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO zone_price_setup (
                website_id, buy_price, buy_price_type_id,
                sell_price, sell_price_type_id, start_date, active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING zone_price_setup_id
            ''', (
                self.website_id, self.buy_price, self.buy_price_type_id,
                self.sell_price, self.sell_price_type_id, self.start_date,
                self.active
            ))
            zone_price_setup_id = cursor.fetchone()[0]
            conn.commit()
            return zone_price_setup_id

    @staticmethod
    def get_all(website_id=None):
        """Get all price setups with related data"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            base_query = """
                WITH latest_prices AS (
                    SELECT DISTINCT ON (
                        zps.website_id,
                        zpm.zone_id,
                        af.format_id
                    )
                        zps.zone_price_setup_id,
                        zps.website_id,
                        zps.buy_price,
                        zps.sell_price,
                        zps.buy_price_type_id,
                        zps.sell_price_type_id,
                        zps.start_date,
                        zps.active as setup_active,
                        zpm.zone_id,
                        zpm.mapping_id,
                        zpm.active as mapping_active,
                        af.format_id
                    FROM zone_price_setup zps
                    JOIN zone_price_mapping zpm ON zps.zone_price_setup_id = zpm.zone_price_setup_id
                    JOIN ads_zone az ON zpm.zone_id = az.zone_id
                    JOIN ads_zone_format azf ON az.zone_id = azf.zone_id
                    JOIN ads_format af ON azf.format_id = af.format_id
                    WHERE zps.active = true 
                    AND zpm.active = true
                    AND az.active = true
                    AND azf.active = true
                    AND af.active = true
                    ORDER BY 
                        zps.website_id,
                        zpm.zone_id,
                        af.format_id,
                        zps.start_date DESC
                )
                SELECT 
                    lp.*,
                    w.domain_website,
                    w.active as website_active,
                    p.email as publisher_email,
                    az.ten_vung_quang_cao as zone_name,
                    az.active as zone_active,
                    az.ma_nhung_vung_quang_cao,
                    azs.size_id,
                    azs.ten_kich_thuoc as size_name,
                    azs.active as size_active,
                    af.format_name,
                    af.campaign_type_id,
                    af.active as format_active,
                    ct.ten_loai_chien_dich as campaign_type_name,
                    ct.active as campaign_type_active,
                    pt1.price_type_name as buy_price_type_name,
                    pt1.active as buy_price_type_active,
                    pt2.price_type_name as sell_price_type_name,
                    pt2.active as sell_price_type_active
                FROM latest_prices lp
                JOIN website w ON lp.website_id = w.website_id
                JOIN publisher p ON w.publisher_id = p.publisher_id
                JOIN ads_zone az ON lp.zone_id = az.zone_id
                LEFT JOIN ads_zone_size azs ON az.size_id = azs.size_id
                JOIN ads_format af ON lp.format_id = af.format_id
                JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                JOIN price_type pt1 ON lp.buy_price_type_id = pt1.price_type_id
                JOIN price_type pt2 ON lp.sell_price_type_id = pt2.price_type_id
            """

            if website_id:
                base_query += " WHERE lp.website_id = %s"
                cursor.execute(base_query + " ORDER BY w.domain_website, az.ten_vung_quang_cao", (website_id,))
            else:
                cursor.execute(base_query + " ORDER BY w.domain_website, az.ten_vung_quang_cao")

            rows = cursor.fetchall()
            if not rows:
                return []

            # Convert rows to dictionaries
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]

            # Group results by website and zone
            grouped_data = {
                'formats': {},
                'zone_prices': {}
            }

            # Group formats by campaign type
            for row in result:
                campaign_type = row['campaign_type_name']
                if campaign_type not in grouped_data['formats']:
                    grouped_data['formats'][campaign_type] = []
                
                format_info = {
                    'format_id': row['format_id'],
                    'format_name': row['format_name']
                }
                if format_info not in grouped_data['formats'][campaign_type]:
                    grouped_data['formats'][campaign_type].append(format_info)

            # Group prices by zone
            for row in result:
                zone_id = row['zone_id']
                if zone_id not in grouped_data['zone_prices']:
                    grouped_data['zone_prices'][zone_id] = {
                        'zone_info': {
                            'zone_id': zone_id,
                            'ten_vung_quang_cao': row['zone_name'],
                            'size_name': row['size_name'],
                            'active': row['zone_active']
                        },
                        'prices': []
                    }

                price_info = {
                    'zone_price_setup_id': row['zone_price_setup_id'],
                    'format_id': row['format_id'],
                    'buy_price': float(row['buy_price']),
                    'sell_price': float(row['sell_price']),
                    'buy_price_type_name': row['buy_price_type_name'],
                    'sell_price_type_name': row['sell_price_type_name'],
                    'start_date': row['start_date'].isoformat(),
                    'mapping_id': row['mapping_id']
                }
                
                if price_info not in grouped_data['zone_prices'][zone_id]['prices']:
                    grouped_data['zone_prices'][zone_id]['prices'].append(price_info)

            return grouped_data

    @staticmethod
    def get_by_id(zone_price_setup_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    zps.*,
                    w.domain_website,
                    p.email,
                    pt1.price_type_name as buy_price_type_name,
                    pt2.price_type_name as sell_price_type_name,
                    az.ten_vung_quang_cao,
                    azs.ten_kich_thuoc as size_name,
                    af.format_name,
                    ct.ten_loai_chien_dich,
                    zpm.mapping_id
                FROM zone_price_setup zps
                LEFT JOIN website w ON zps.website_id = w.website_id
                LEFT JOIN publisher p ON w.publisher_id = p.publisher_id
                LEFT JOIN price_type pt1 ON zps.buy_price_type_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON zps.sell_price_type_id = pt2.price_type_id
                LEFT JOIN zone_price_mapping zpm ON zps.zone_price_setup_id = zpm.zone_price_setup_id
                LEFT JOIN ads_zone az ON zpm.zone_id = az.zone_id
                LEFT JOIN ads_zone_size azs ON az.size_id = azs.size_id
                LEFT JOIN ads_zone_format azf ON az.zone_id = azf.zone_id
                LEFT JOIN ads_format af ON azf.format_id = af.format_id
                LEFT JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                WHERE zps.zone_price_setup_id = %s
            ''', (zone_price_setup_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return ZonePriceSetup._format_row(dict(zip([column[0] for column in cursor.description], row)))

    @staticmethod
    def get_by_website_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    zps.*,
                    w.domain_website,
                    p.email,
                    pt1.price_type_name as buy_price_type_name,
                    pt2.price_type_name as sell_price_type_name,
                    az.ten_vung_quang_cao,
                    azs.ten_kich_thuoc as size_name,
                    af.format_name,
                    ct.ten_loai_chien_dich,
                    zpm.mapping_id
                FROM zone_price_setup zps
                LEFT JOIN website w ON zps.website_id = w.website_id
                LEFT JOIN publisher p ON w.publisher_id = p.publisher_id
                LEFT JOIN price_type pt1 ON zps.buy_price_type_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON zps.sell_price_type_id = pt2.price_type_id
                LEFT JOIN zone_price_mapping zpm ON zps.zone_price_setup_id = zpm.zone_price_setup_id
                LEFT JOIN ads_zone az ON zpm.zone_id = az.zone_id
                LEFT JOIN ads_zone_size azs ON az.size_id = azs.size_id
                LEFT JOIN ads_zone_format azf ON az.zone_id = azf.zone_id
                LEFT JOIN ads_format af ON azf.format_id = af.format_id
                LEFT JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                WHERE zps.website_id = %s
                ORDER BY zps.created_at DESC
            ''', (website_id,))
            rows = cursor.fetchall()
            return [ZonePriceSetup._format_row(dict(zip([column[0] for column in cursor.description], row)))
                    for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE zone_price_setup 
            SET website_id = %s,
                buy_price = %s,
                buy_price_type_id = %s,
                sell_price = %s,
                sell_price_type_id = %s,
                start_date = %s,
                updated_at = CURRENT_TIMESTAMP,
                active = %s
            WHERE zone_price_setup_id = %s
            ''', (
                self.website_id, self.buy_price, self.buy_price_type_id,
                self.sell_price, self.sell_price_type_id, self.start_date,
                self.active, self.zone_price_setup_id
            ))
            conn.commit()

    @staticmethod
    def delete_by_id(zone_price_setup_id):
        """Soft delete a price record"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE zone_price_setup 
            SET active = false,
                updated_at = CURRENT_TIMESTAMP
            WHERE zone_price_setup_id = %s
            ''', (zone_price_setup_id,))
            conn.commit()

    @staticmethod
    def get_price_summary(website_id):
        """Get price statistics for a website's zones"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_prices,
                    AVG(buy_price) as avg_buy_price,
                    AVG(sell_price) as avg_sell_price,
                    MIN(start_date) as earliest_price,
                    MAX(start_date) as latest_price,
                    COUNT(DISTINCT zpm.zone_id) as total_zones
                FROM zone_price_setup zps
                LEFT JOIN zone_price_mapping zpm ON zps.zone_price_setup_id = zpm.zone_price_setup_id
                WHERE zps.website_id = %s
            ''', (website_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return ZonePriceSetup._format_row(dict(zip([column[0] for column in cursor.description], row)))
