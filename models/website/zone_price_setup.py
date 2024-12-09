from configs.db import get_db_connection
class ZonePriceSetup:
    def __init__(self, zone_price_setup_id=None, website_id=None,
                 buy_price=0, buy_price_type_id=None,
                 sell_price=0, sell_price_type_id=None,
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
                buy_price DECIMAL(15,2),
                buy_price_type_id INTEGER,
                sell_price DECIMAL(15,2),
                sell_price_type_id INTEGER,
                start_date DATE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (website_id) REFERENCES website(website_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (buy_price_type_id) REFERENCES price_type(price_type_id)
                    ON DELETE SET NULL,
                FOREIGN KEY (sell_price_type_id) REFERENCES price_type(price_type_id)
                    ON DELETE SET NULL
            )
            ''')
            conn.commit() 