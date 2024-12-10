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
            
    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO zone_price_mapping (
                zone_price_setup_id, zone_id
            )
            VALUES (
                %s, %s
            )
            ''', (
                self.zone_price_setup_id, self.zone_id
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM zone_price_mapping
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(mapping_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM zone_price_mapping WHERE mapping_id = %s', (mapping_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def update(mapping_id, data={}):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build update query dynamically based on provided fields
            update_fields = []
            params = []
            
            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)
                    
            if update_fields:
                query = f'''
                UPDATE zone_price_mapping 
                SET {', '.join(update_fields)}
                WHERE mapping_id = %s;
                '''
                params.append(mapping_id)
                
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(mapping_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM zone_price_mapping WHERE mapping_id = %s
            ''', (mapping_id,))
            conn.commit()
