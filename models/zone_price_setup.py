from configs.db import get_db_connection


class ZonePriceSetup:
    def __init__(self, zone_price_setup_id=None, website_id=None,
                 buy_price=0.0, buy_price_type_id=None,
                 sell_price=0.0, sell_price_type_id=None,
                 start_date=None, created_at=None, updated_at=None):
        self.zone_price_setup_id = zone_price_setup_id
        self.website_id = website_id
        self.buy_price = buy_price
        self.buy_price_type_id = buy_price_type_id
        self.sell_price = sell_price
        self.sell_price_type_id = sell_price_type_id
        self.start_date = start_date
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS zone_price_setup (
                zone_price_setup_id SERIAL PRIMARY KEY,
                website_id INTEGER NOT NULL,
                buy_price REAL NOT NULL,
                buy_price_type_id INTEGER NOT NULL,
                sell_price REAL NOT NULL,
                sell_price_type_id INTEGER NOT NULL,
                start_date TIMESTAMPTZ NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
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
                sell_price, sell_price_type_id, start_date
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                self.website_id, self.buy_price, self.buy_price_type_id,
                self.sell_price, self.sell_price_type_id, self.start_date
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zps.*,
                       w.website_name,
                       pt1.price_type_name as buy_price_type_name,
                       pt2.price_type_name as sell_price_type_name
                FROM zone_price_setup zps
                LEFT JOIN website w ON zps.website_id = w.website_id
                LEFT JOIN price_type pt1 ON zps.buy_price_type_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON zps.sell_price_type_id = pt2.price_type_id
                ORDER BY zps.created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row))
                    for row in rows]

    @staticmethod
    def get_by_id(zone_price_setup_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zps.*,
                       w.website_name,
                       pt1.price_type_name as buy_price_type_name,
                       pt2.price_type_name as sell_price_type_name
                FROM zone_price_setup zps
                LEFT JOIN website w ON zps.website_id = w.website_id
                LEFT JOIN price_type pt1 ON zps.buy_price_type_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON zps.sell_price_type_id = pt2.price_type_id
                WHERE zps.zone_price_setup_id = %s
            ''', (zone_price_setup_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_website_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zps.*,
                       w.website_name,
                       pt1.price_type_name as buy_price_type_name,
                       pt2.price_type_name as sell_price_type_name
                FROM zone_price_setup zps
                LEFT JOIN website w ON zps.website_id = w.website_id
                LEFT JOIN price_type pt1 ON zps.buy_price_type_id = pt1.price_type_id
                LEFT JOIN price_type pt2 ON zps.sell_price_type_id = pt2.price_type_id
                WHERE zps.website_id = %s
                ORDER BY zps.created_at DESC
            ''', (website_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row))
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
                updated_at = CURRENT_TIMESTAMP
            WHERE zone_price_setup_id = %s
            ''', (
                self.website_id, self.buy_price, self.buy_price_type_id,
                self.sell_price, self.sell_price_type_id, self.start_date,
                self.zone_price_setup_id
            ))
            conn.commit()
