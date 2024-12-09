from configs.db import get_db_connection
class ZonePriceMapping:
    def __init__(self, mapping_id=None, zone_price_setup_id=None, zone_id=None):
        self.mapping_id = mapping_id
        self.zone_price_setup_id = zone_price_setup_id
        self.zone_id = zone_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS zone_price_mapping (
                mapping_id SERIAL PRIMARY KEY,
                zone_price_setup_id INTEGER NOT NULL,
                zone_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (zone_price_setup_id) REFERENCES zone_price_setup(zone_price_setup_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (zone_id) REFERENCES ads_zone(zone_id)
                    ON DELETE CASCADE,
                UNIQUE(zone_price_setup_id, zone_id)
            )
            ''')
            conn.commit() 