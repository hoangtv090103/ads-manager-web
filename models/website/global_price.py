from configs.db import get_db_connection
class GlobalPrice:
    def __init__(self, global_price_id=None, price_setup_id=None, website_id=None,
                 is_uniform_price=False, uniform_buy_price=0, uniform_sell_price=0,
                 uniform_buy_price_unit_id=None, uniform_sell_price_unit_id=None,
                 ad_format_id=None, buy_price=0, buy_price_unit_id=None,
                 sell_price=0, sell_price_unit_id=None, start_date=None):
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