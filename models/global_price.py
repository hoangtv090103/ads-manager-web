from configs.db import get_db_connection


class GlobalPrice:
    def __init__(self, global_price_id=None, price_setup_id=None, website_id=None,
                 is_uniform_price=False, uniform_buy_price=0, uniform_sell_price=0,
                 uniform_buy_price_unit_id=None, uniform_sell_price_unit_id=None,
                 ad_format_id=None, buy_price=0, buy_price_unit_id=None,
                 sell_price=0, sell_price_unit_id=None, start_date=None,
                 created_at=None, updated_at=None, active=True):
        self.global_price_id = global_price_id
        self.price_setup_id = price_setup_id
        self.website_id = website_id
        self.is_uniform_price = is_uniform_price
        self.uniform_buy_price = uniform_buy_price
        self.uniform_sell_price = uniform_sell_price
        self.uniform_buy_price_unit_id = uniform_buy_price_unit_id
        self.uniform_sell_price_unit_id = uniform_sell_price_unit_id
        self.ad_format_id = ad_format_id
        self.buy_price = buy_price
        self.buy_price_unit_id = buy_price_unit_id
        self.sell_price = sell_price
        self.sell_price_unit_id = sell_price_unit_id
        self.start_date = start_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_price (
                global_price_id SERIAL PRIMARY KEY,
                price_setup_id INTEGER NOT NULL,
                website_id INTEGER NOT NULL,
                is_uniform_price BOOLEAN DEFAULT FALSE,
                uniform_buy_price DECIMAL(15,2),
                uniform_sell_price DECIMAL(15,2),
                uniform_buy_price_unit_id INTEGER,
                uniform_sell_price_unit_id INTEGER,
                ad_format_id INTEGER,
                buy_price DECIMAL(15,2),
                buy_price_unit_id INTEGER,
                sell_price DECIMAL(15,2),
                sell_price_unit_id INTEGER,
                start_date DATE,
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
                    ON DELETE SET NULL
            )
            ''')
            conn.commit()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO global_price (
                price_setup_id, website_id, is_uniform_price,
                uniform_buy_price, uniform_sell_price,
                uniform_buy_price_unit_id, uniform_sell_price_unit_id,
                ad_format_id, buy_price, buy_price_unit_id,
                sell_price, sell_price_unit_id, start_date, active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                self.price_setup_id, self.website_id, self.is_uniform_price,
                self.uniform_buy_price, self.uniform_sell_price,
                self.uniform_buy_price_unit_id, self.uniform_sell_price_unit_id,
                self.ad_format_id, self.buy_price, self.buy_price_unit_id,
                self.sell_price, self.sell_price_unit_id, self.start_date,
                self.active
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT gp.*, w.website_name,
                       pt1.price_type_name as uniform_buy_price_type,
                       pt2.price_type_name as uniform_sell_price_type,
                       pt3.price_type_name as buy_price_type,
                       pt4.price_type_name as sell_price_type
                FROM global_price gp
                LEFT JOIN website w ON gp.website_id = w.website_id
                LEFT JOIN price_type pt1 ON gp.uniform_buy_price_unit_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON gp.uniform_sell_price_unit_id = pt2.price_type_id
                LEFT JOIN price_type pt3 ON gp.buy_price_unit_id = pt3.price_type_id
                LEFT JOIN price_type pt4 ON gp.sell_price_unit_id = pt4.price_type_id
                WHERE gp.active = true
                ORDER BY gp.created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row))
                    for row in rows]

    @staticmethod
    def get_by_id(global_price_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT gp.*, w.website_name,
                       pt1.price_type_name as uniform_buy_price_type,
                       pt2.price_type_name as uniform_sell_price_type,
                       pt3.price_type_name as buy_price_type,
                       pt4.price_type_name as sell_price_type
                FROM global_price gp
                LEFT JOIN website w ON gp.website_id = w.website_id
                LEFT JOIN price_type pt1 ON gp.uniform_buy_price_unit_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON gp.uniform_sell_price_unit_id = pt2.price_type_id
                LEFT JOIN price_type pt3 ON gp.buy_price_unit_id = pt3.price_type_id
                LEFT JOIN price_type pt4 ON gp.sell_price_unit_id = pt4.price_type_id
                WHERE gp.global_price_id = %s
            ''', (global_price_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_website_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT gp.*, w.website_name,
                       pt1.price_type_name as uniform_buy_price_type,
                       pt2.price_type_name as uniform_sell_price_type,
                       pt3.price_type_name as buy_price_type,
                       pt4.price_type_name as sell_price_type
                FROM global_price gp
                LEFT JOIN website w ON gp.website_id = w.website_id
                LEFT JOIN price_type pt1 ON gp.uniform_buy_price_unit_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON gp.uniform_sell_price_unit_id = pt2.price_type_id
                LEFT JOIN price_type pt3 ON gp.buy_price_unit_id = pt3.price_type_id
                LEFT JOIN price_type pt4 ON gp.sell_price_unit_id = pt4.price_type_id
                WHERE gp.website_id = %s AND gp.active = true
            ''', (website_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row))
                    for row in rows]

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE global_price 
            SET price_setup_id = %s,
                website_id = %s,
                is_uniform_price = %s,
                uniform_buy_price = %s,
                uniform_sell_price = %s,
                uniform_buy_price_unit_id = %s,
                uniform_sell_price_unit_id = %s,
                ad_format_id = %s,
                buy_price = %s,
                buy_price_unit_id = %s,
                sell_price = %s,
                sell_price_unit_id = %s,
                start_date = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE global_price_id = %s
            ''', (
                self.price_setup_id, self.website_id, self.is_uniform_price,
                self.uniform_buy_price, self.uniform_sell_price,
                self.uniform_buy_price_unit_id, self.uniform_sell_price_unit_id,
                self.ad_format_id, self.buy_price, self.buy_price_unit_id,
                self.sell_price, self.sell_price_unit_id, self.start_date,
                self.global_price_id
            ))
            conn.commit()

    @staticmethod
    def delete_by_id(global_price_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE global_price 
            SET active = false,
                updated_at = CURRENT_TIMESTAMP
            WHERE global_price_id = %s
            ''', (global_price_id,))
            conn.commit()

    @staticmethod
    def get_price_summary(website_id):
        """Get price statistics for a website"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_prices,
                    AVG(buy_price) as avg_buy_price,
                    AVG(sell_price) as avg_sell_price,
                    MIN(start_date) as earliest_price,
                    MAX(start_date) as latest_price
                FROM global_price
                WHERE website_id = %s AND active = true
            ''', (website_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row)) 