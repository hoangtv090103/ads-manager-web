from configs.db import get_db_connection

class ZonePriceSetup:
    def __init__(self, zone_price_setup_id=None, pricetype_id=None, zone_id=None):
        self.zone_price_setup_id = zone_price_setup_id
        self.pricetype_id = pricetype_id
        self.zone_id = zone_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS zone_price_setup_detail (
                zone_price_setup_id INTEGER NOT NULL,
                pricetype_id INTEGER NOT NULL,
                zone_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (zone_price_setup_id, pricetype_id, zone_id),
                FOREIGN KEY (zone_price_setup_id) REFERENCES zone_price_setup(id),
                FOREIGN KEY (pricetype_id) REFERENCES price_type(pricetype_id),
                FOREIGN KEY (zone_id) REFERENCES ads_zone(zone_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO zone_price_setup_detail (
                zone_price_setup_id, pricetype_id, zone_id
            )
            VALUES (%s, %s, %s)
            ''', (
                self.zone_price_setup_id, self.pricetype_id, self.zone_id
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zpsd.*,
                       zps.ten as setup_name,
                       pt.ten_loai_gia as price_type_name,
                       az.ten_vung_quang_cao as zone_name
                FROM zone_price_setup_detail zpsd
                JOIN zone_price_setup zps ON zpsd.zone_price_setup_id = zps.id
                JOIN price_type pt ON zpsd.pricetype_id = pt.pricetype_id
                JOIN ads_zone az ON zpsd.zone_id = az.zone_id
                WHERE zpsd.active = TRUE
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_setup_id(zone_price_setup_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zpsd.*,
                       zps.ten as setup_name,
                       pt.ten_loai_gia as price_type_name,
                       az.ten_vung_quang_cao as zone_name
                FROM zone_price_setup_detail zpsd
                JOIN zone_price_setup zps ON zpsd.zone_price_setup_id = zps.id
                JOIN price_type pt ON zpsd.pricetype_id = pt.pricetype_id
                JOIN ads_zone az ON zpsd.zone_id = az.zone_id
                WHERE zpsd.zone_price_setup_id = %s AND zpsd.active = TRUE
            ''', (zone_price_setup_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def delete(zone_price_setup_id, pricetype_id, zone_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE zone_price_setup_detail 
            SET active = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE zone_price_setup_id = %s 
            AND pricetype_id = %s 
            AND zone_id = %s
            ''', (zone_price_setup_id, pricetype_id, zone_id))
            conn.commit()
