from configs.db import get_db_connection
from datetime import datetime, date
from models.website import Website
from models.ads_format import AdsFormat
from models.price_type import PriceType
from decimal import Decimal


def format_value(value):
    """Format values for JSON serialization"""
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


class GlobalPrice:
    def __init__(self, global_price_id=None, website_id=None,
                 is_uniform_price=False, uniform_buy_price=0, uniform_sell_price=0,
                 uniform_buy_price_unit_id=None, uniform_sell_price_unit_id=None,
                 format_id=None, buy_price=0, buy_price_unit_id=None,
                 sell_price=0, sell_price_unit_id=None, start_date=None,
                 created_at=None, updated_at=None, active=True):
        self.global_price_id = global_price_id
        self.website_id = website_id
        self.is_uniform_price = is_uniform_price
        self.uniform_buy_price = uniform_buy_price
        self.uniform_sell_price = uniform_sell_price
        self.uniform_buy_price_unit_id = uniform_buy_price_unit_id
        self.uniform_sell_price_unit_id = uniform_sell_price_unit_id
        self.format_id = format_id
        self.buy_price = buy_price
        self.buy_price_unit_id = buy_price_unit_id
        self.sell_price = sell_price
        self.sell_price_unit_id = sell_price_unit_id
        self.start_date = start_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.active = active

    def validate(self):
        """Validate all fields and relationships before saving"""
        errors = []

        # Check required fields
        if not self.website_id:
            errors.append("Website ID is required")
        if not self.start_date:
            errors.append("Start date is required")

        # Validate website exists
        if self.website_id:
            website = Website.get_by_id(self.website_id)
            if not website:
                errors.append(
                    f"Website with ID {self.website_id} does not exist")

        # Validate format exists if specified
        if self.format_id:
            format = AdsFormat.get_by_id(self.format_id)
            if not format:
                errors.append(
                    f"Format with ID {self.format_id} does not exist")

        # Validate price types exist
        price_types = []
        if self.uniform_buy_price_unit_id:
            price_type = PriceType.get_by_id(self.uniform_buy_price_unit_id)
            if not price_type:
                errors.append(
                    f"Price type with ID {self.uniform_buy_price_unit_id} does not exist")
            price_types.append(price_type)

        if self.uniform_sell_price_unit_id:
            price_type = PriceType.get_by_id(self.uniform_sell_price_unit_id)
            if not price_type:
                errors.append(
                    f"Price type with ID {self.uniform_sell_price_unit_id} does not exist")
            price_types.append(price_type)

        if self.buy_price_unit_id:
            price_type = PriceType.get_by_id(self.buy_price_unit_id)
            if not price_type:
                errors.append(
                    f"Price type with ID {self.buy_price_unit_id} does not exist")
            price_types.append(price_type)

        if self.sell_price_unit_id:
            price_type = PriceType.get_by_id(self.sell_price_unit_id)
            if not price_type:
                errors.append(
                    f"Price type with ID {self.sell_price_unit_id} does not exist")
            price_types.append(price_type)

        # Validate price values
        if self.uniform_buy_price < 0:
            errors.append("Uniform buy price cannot be negative")
        if self.uniform_sell_price < 0:
            errors.append("Uniform sell price cannot be negative")
        if self.buy_price < 0:
            errors.append("Buy price cannot be negative")
        if self.sell_price < 0:
            errors.append("Sell price cannot be negative")

        # Check for existing active price for same website/format combination
        if self.format_id and not self.global_price_id:  # Only for new records
            existing = self.get_active_by_website_format(
                self.website_id, self.format_id)
            if existing:
                errors.append(
                    f"Active price already exists for website {self.website_id} and format {self.format_id}")

        if errors:
            raise ValueError("\n".join(errors))

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_price (
                global_price_id SERIAL PRIMARY KEY,
                website_id INTEGER NOT NULL,
                is_uniform_price BOOLEAN DEFAULT FALSE,
                uniform_buy_price DECIMAL(15,2),
                uniform_sell_price DECIMAL(15,2),
                uniform_buy_price_unit_id INTEGER,
                uniform_sell_price_unit_id INTEGER,
                format_id INTEGER,
                buy_price DECIMAL(15,2),
                buy_price_unit_id INTEGER,
                sell_price DECIMAL(15,2),
                sell_price_unit_id INTEGER,
                start_date DATE NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (uniform_buy_price_unit_id) REFERENCES price_type(price_type_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (uniform_sell_price_unit_id) REFERENCES price_type(price_type_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (buy_price_unit_id) REFERENCES price_type(price_type_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (sell_price_unit_id) REFERENCES price_type(price_type_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE SET NULL
            )
            ''')
            conn.commit()

    def save(self):
        try:
            # Validate before saving
            # self.validate()

            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO global_price (
                    website_id, is_uniform_price,
                    uniform_buy_price, uniform_sell_price,
                    uniform_buy_price_unit_id, uniform_sell_price_unit_id,
                    format_id, buy_price, buy_price_unit_id,
                    sell_price, sell_price_unit_id, start_date, active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING global_price_id
                ''', (
                    self.website_id, self.is_uniform_price,
                    self.uniform_buy_price, self.uniform_sell_price,
                    self.uniform_buy_price_unit_id, self.uniform_sell_price_unit_id,
                    self.format_id, self.buy_price, self.buy_price_unit_id,
                    self.sell_price, self.sell_price_unit_id, self.start_date,
                    self.active
                ))
                row = cursor.fetchone()
                if not row:
                    raise Exception("Failed to create global price")
                global_price_id = row[0]
                conn.commit()
                return global_price_id
        except Exception as e:
            raise Exception(f"Error saving global price: {str(e)}")

    @staticmethod
    def _format_row(row_dict):
        """Format a row dictionary for JSON serialization"""
        return {key: format_value(value) for key, value in row_dict.items()}

    @staticmethod
    def get_all(website_id=None):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                base_query = """
                    WITH latest_prices AS (
                        SELECT DISTINCT ON (
                            gp.website_id,
                            gp.format_id
                        )
                            gp.*
                        FROM global_price gp
                        WHERE gp.active = true
                        ORDER BY 
                            gp.website_id,
                            gp.format_id,
                            gp.start_date DESC
                    )
                    SELECT 
                        lp.*,
                        w.domain_website,
                        w.active as website_active,
                        p.email as publisher_email,
                        af.format_name,
                        af.campaign_type_id,
                        af.active as format_active,
                        ct.ten_loai_chien_dich as campaign_type_name,
                        ct.active as campaign_type_active
                    FROM latest_prices lp
                    JOIN website w ON lp.website_id = w.website_id
                    JOIN publisher p ON w.publisher_id = p.publisher_id
                    JOIN ads_format af ON lp.format_id = af.format_id
                    JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                """

                if website_id:
                    base_query += " WHERE lp.website_id = %s"
                    cursor.execute(base_query + " ORDER BY w.domain_website, af.format_name", (website_id,))
                else:
                    cursor.execute(base_query + " ORDER BY w.domain_website, af.format_name")

                rows = cursor.fetchall()
                if not rows:
                    return {'formats': {}, 'website_prices': {}}

                # Convert rows to dictionaries
                columns = [desc[0] for desc in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]

                # Group results by website and format type
                grouped_data = {
                    'formats': {},
                    'website_prices': {}
                }

                # Group formats by campaign type
                for row in result:
                    campaign_type = row['campaign_type_name']
                    if campaign_type not in grouped_data['formats']:
                        grouped_data['formats'][campaign_type] = []
                    
                    format_info = {
                        'format_id': row['format_id'],
                        'format_name': row['format_name'],
                        'campaign_type_id': row['campaign_type_id']
                    }
                    if format_info not in grouped_data['formats'][campaign_type]:
                        grouped_data['formats'][campaign_type].append(format_info)

                # Group prices by website
                for row in result:
                    website_id = row['website_id']
                    if website_id not in grouped_data['website_prices']:
                        grouped_data['website_prices'][website_id] = {
                            'website_info': {
                                'website_id': website_id,
                                'domain_website': row['domain_website'],
                                'publisher_email': row['publisher_email'],
                                'active': row['website_active']
                            },
                            'prices': []
                        }

                    price_info = {
                        'global_price_id': row['global_price_id'],
                        'format_id': row['format_id'],
                        'format_name': row['format_name'],
                        'campaign_type_name': row['campaign_type_name'],
                        'is_uniform_price': row['is_uniform_price'],
                        'uniform_buy_price': float(row['uniform_buy_price']) if row['uniform_buy_price'] else 0,
                        'uniform_sell_price': float(row['uniform_sell_price']) if row['uniform_sell_price'] else 0,
                        'buy_price': float(row['buy_price']) if row['buy_price'] else 0,
                        'sell_price': float(row['sell_price']) if row['sell_price'] else 0,
                        'start_date': row['start_date'].isoformat(),
                        'active': row['active']
                    }
                    
                    if price_info not in grouped_data['website_prices'][website_id]['prices']:
                        grouped_data['website_prices'][website_id]['prices'].append(price_info)

                return grouped_data

        except Exception as e:
            if "out of range" in str(e):
                raise Exception("Invalid date value in database. Please check the date ranges.")
            raise e

    @staticmethod
    def get_by_id(global_price_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT gp.*, w.domain_website, p.email,
                       pt1.price_type_name as uniform_buy_price_type,
                       pt2.price_type_name as uniform_sell_price_type,
                       pt3.price_type_name as buy_price_type,
                       pt4.price_type_name as sell_price_type,
                       af.format_name,
                       ct.ten_loai_chien_dich
                FROM global_price gp
                LEFT JOIN website w ON gp.website_id = w.website_id
                LEFT JOIN publisher p ON w.publisher_id = p.publisher_id
                LEFT JOIN price_type pt1 ON gp.uniform_buy_price_unit_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON gp.uniform_sell_price_unit_id = pt2.price_type_id
                LEFT JOIN price_type pt3 ON gp.buy_price_unit_id = pt3.price_type_id
                LEFT JOIN price_type pt4 ON gp.sell_price_unit_id = pt4.price_type_id
                LEFT JOIN ads_format af ON gp.format_id = af.format_id
                LEFT JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                WHERE gp.global_price_id = %s
            ''', (global_price_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return GlobalPrice._format_row(dict(zip([column[0] for column in cursor.description], row)))

    @staticmethod
    def get_by_website_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT gp.*, w.domain_website, p.email,
                       pt1.price_type_name as uniform_buy_price_type,
                       pt2.price_type_name as uniform_sell_price_type,
                       pt3.price_type_name as buy_price_type,
                       pt4.price_type_name as sell_price_type,
                       af.format_name,
                       ct.ten_loai_chien_dich
                FROM global_price gp
                LEFT JOIN website w ON gp.website_id = w.website_id
                LEFT JOIN publisher p ON w.publisher_id = p.publisher_id
                LEFT JOIN price_type pt1 ON gp.uniform_buy_price_unit_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON gp.uniform_sell_price_unit_id = pt2.price_type_id
                LEFT JOIN price_type pt3 ON gp.buy_price_unit_id = pt3.price_type_id
                LEFT JOIN price_type pt4 ON gp.sell_price_unit_id = pt4.price_type_id
                LEFT JOIN ads_format af ON gp.format_id = af.format_id
                LEFT JOIN campaign_type ct ON af.campaign_type_id = ct.camp_type_id
                WHERE gp.website_id = %s AND gp.active = true
                ORDER BY gp.created_at DESC
            ''', (website_id,))
            rows = cursor.fetchall()
            return [GlobalPrice._format_row(dict(zip([column[0] for column in cursor.description], row)))
                    for row in rows]

    @staticmethod
    def get_active_by_website_format(website_id, format_id):
        """Get active price for a specific website and format combination"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT gp.*, w.domain_website, p.email,
                       pt1.price_type_name as uniform_buy_price_type,
                       pt2.price_type_name as uniform_sell_price_type,
                       pt3.price_type_name as buy_price_type,
                       pt4.price_type_name as sell_price_type,
                       af.format_name,
                       ct.ten_loai_chien_dich
                FROM global_price gp
                LEFT JOIN website w ON gp.website_id = w.website_id
                LEFT JOIN publisher p ON w.publisher_id = p.publisher_id
                WHERE gp.website_id = %s AND gp.format_id = %s AND gp.active = true
            ''', (website_id, format_id))
            row = cursor.fetchone()
            if not row:
                return None
            return GlobalPrice._format_row(dict(zip([column[0] for column in cursor.description], row)))

    def update(self):
        try:
            # Validate before updating
            self.validate()

            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE global_price 
                SET website_id = %s,
                    is_uniform_price = %s,
                    uniform_buy_price = %s,
                    uniform_sell_price = %s,
                    uniform_buy_price_unit_id = %s,
                    uniform_sell_price_unit_id = %s,
                    format_id = %s,
                    buy_price = %s,
                    buy_price_unit_id = %s,
                    sell_price = %s,
                    sell_price_unit_id = %s,
                    start_date = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE global_price_id = %s
                ''', (
                    self.website_id, self.is_uniform_price,
                    self.uniform_buy_price, self.uniform_sell_price,
                    self.uniform_buy_price_unit_id, self.uniform_sell_price_unit_id,
                    self.format_id, self.buy_price, self.buy_price_unit_id,
                    self.sell_price, self.sell_price_unit_id, self.start_date,
                    self.global_price_id
                ))
                if cursor.rowcount == 0:
                    raise Exception("No rows updated")
                conn.commit()
        except Exception as e:
            raise Exception(f"Error updating global price: {str(e)}")

    @staticmethod
    def delete_by_id(global_price_id):
        """Soft delete a price record"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE global_price 
            SET active = false,
                updated_at = CURRENT_TIMESTAMP
            WHERE global_price_id = %s
            ''', (global_price_id,))
            if cursor.rowcount == 0:
                raise Exception("No rows deleted")
            conn.commit()

    @staticmethod
    def get_price_summary(website_id):
        """Get price statistics for a website"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_prices,
                    AVG(CASE WHEN is_uniform_price THEN uniform_buy_price ELSE buy_price END) as avg_buy_price,
                    AVG(CASE WHEN is_uniform_price THEN uniform_sell_price ELSE sell_price END) as avg_sell_price,
                    MIN(start_date) as earliest_price,
                    MAX(start_date) as latest_price,
                    COUNT(DISTINCT format_id) as total_formats
                FROM global_price
                WHERE website_id = %s AND active = true
            ''', (website_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return GlobalPrice._format_row(dict(zip([column[0] for column in cursor.description], row)))
