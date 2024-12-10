from configs.db import get_db_connection

class ZonePrice:
    def __init__(self, id=None, zone_price_setup_id=None, zone_id=None,
                 pricestatus_id=None, format_id=None, gia_mua=0, gia_ban=0, status=1):
        self.id = id
        self.zone_price_setup_id = zone_price_setup_id
        self.zone_id = zone_id
        self.pricestatus_id = pricestatus_id
        self.format_id = format_id
        self.gia_mua = gia_mua
        self.gia_ban = gia_ban
        self.status = status

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS zone_price (
                id SERIAL PRIMARY KEY,
                zone_price_setup_id INTEGER NOT NULL,
                zone_id INTEGER NOT NULL,
                pricestatus_id INTEGER NOT NULL,
                format_id INTEGER NOT NULL,
                gia_mua DECIMAL,
                gia_ban DECIMAL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                status INTEGER DEFAULT 1,
                FOREIGN KEY (zone_price_setup_id) REFERENCES zone_price_setup(id),
                FOREIGN KEY (zone_id) REFERENCES ads_zone(zone_id),
                FOREIGN KEY (pricestatus_id) REFERENCES price_status(pricestatus_id),
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO zone_price (
                zone_price_setup_id, zone_id, pricestatus_id, 
                format_id, gia_mua, gia_ban, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            ''', (
                self.zone_price_setup_id, self.zone_id, self.pricestatus_id,
                self.format_id, self.gia_mua, self.gia_ban, self.status
            ))
            self.id = cursor.fetchone()[0]
            conn.commit()
            return self.id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zp.*, 
                       az.ten_vung_quang_cao,
                       ps.ten_trang_thai as price_status,
                       f.ten_dinh_dang as format_name,
                       zps.ten as setup_name
                FROM zone_price zp
                JOIN ads_zone az ON zp.zone_id = az.zone_id
                JOIN price_status ps ON zp.pricestatus_id = ps.pricestatus_id
                JOIN format f ON zp.format_id = f.format_id
                JOIN zone_price_setup zps ON zp.zone_price_setup_id = zps.id
                WHERE zp.status = 1
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT zp.*, 
                       az.ten_vung_quang_cao,
                       ps.ten_trang_thai as price_status,
                       f.ten_dinh_dang as format_name,
                       zps.ten as setup_name
                FROM zone_price zp
                JOIN ads_zone az ON zp.zone_id = az.zone_id
                JOIN price_status ps ON zp.pricestatus_id = ps.pricestatus_id
                JOIN format f ON zp.format_id = f.format_id
                JOIN zone_price_setup zps ON zp.zone_price_setup_id = zps.id
                WHERE zp.id = %s AND zp.status = 1
            ''', (id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def update(id, data):
        with get_db_connection() as conn:
            cursor = conn.cursor()

            update_fields = []
            params = []

            for field, value in data.items():
                if field not in ['id', 'created_at']:
                    update_fields.append(f"{field} = %s")
                    params.append(value)

            if update_fields:
                query = f'''
                UPDATE zone_price 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND status = 1
                '''
                params.append(id)

                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE zone_price 
            SET status = 0, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            ''', (id,))
            conn.commit()
