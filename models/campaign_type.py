from configs.db import get_db_connection


class CampaignType:
    def __init__(self, camp_type_id=None, ten_loai_chien_dich=""):
        self.camp_type_id = camp_type_id
        self.ten_loai_chien_dich = ten_loai_chien_dich

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_type (
                camp_type_id SERIAL PRIMARY KEY,
                ten_loai_chien_dich VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE
            )
            ''')
            conn.commit()

            # Check if table exists before querying
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'campaign_type'
                )
            """)
            table_exists = cursor.fetchone()[0]

            if table_exists:
                cursor.execute('SELECT COUNT(*) FROM campaign_type')
                count = cursor.fetchone()[0]
                
                if count == 0:
                    # Tạo dữ liệu mặc định
                    cursor.execute('''
                        INSERT INTO campaign_type (ten_loai_chien_dich)
                        VALUES ('Display Ads'), ('Native Ads'), ('Ecommerce')
                        ON CONFLICT DO NOTHING
                    ''')
                    conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO campaign_type (ten_loai_chien_dich)
            VALUES (%s)
            RETURNING camp_type_id
            ''', (self.ten_loai_chien_dich,))
            self.camp_type_id = cursor.fetchone()[0]
            conn.commit()
            return self.camp_type_id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT camp_type_id, ten_loai_chien_dich, created_at, updated_at, active
                FROM campaign_type 
                WHERE active = TRUE
            ''')
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(camp_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT camp_type_id, ten_loai_chien_dich, created_at, updated_at, active
                FROM campaign_type 
                WHERE camp_type_id = %s AND active = TRUE
            ''', (camp_type_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_name(ten_loai_chien_dich):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT camp_type_id FROM campaign_type WHERE ten_loai_chien_dich = %s
            ''', (ten_loai_chien_dich,))
            row = cursor.fetchone()
            return row[0] if row else None
            

    @staticmethod
    def update(camp_type_id, data={}):
        with get_db_connection() as conn:
            cursor = conn.cursor()

            update_fields = []
            params = []

            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)

            if update_fields:
                query = f'''
                UPDATE campaign_type 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE camp_type_id = %s AND active = TRUE
                '''
                params.append(camp_type_id)

                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(camp_type_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE campaign_type SET active = FALSE 
            WHERE camp_type_id = %s
            ''', (camp_type_id,))
            conn.commit()
