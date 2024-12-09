from configs.db import get_db_connection



class GlobalPrice:
    def __init__(self, id=None, pricetype_id=None, format_id=None,
                 dong_nhat_gia=None, gia_mua=None, gia_ban=None):
        self.id = id
        self.pricetype_id = pricetype_id
        self.format_id = format_id
        self.dong_nhat_gia = dong_nhat_gia
        self.gia_mua = gia_mua
        self.gia_ban = gia_ban

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_price (
                id SERIAL PRIMARY KEY,
                pricetype_id INTEGER,
                format_id INTEGER,
                dong_nhat_gia INTEGER,
                gia_mua FLOAT,
                gia_ban FLOAT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (pricetype_id) REFERENCES price_type(pricetype_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (format_id) REFERENCES ads_format(format_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO global_price (
                pricetype_id, format_id, dong_nhat_gia,
                gia_mua, gia_ban
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            ''', (
                self.pricetype_id, self.format_id, self.dong_nhat_gia,
                self.gia_mua, self.gia_ban
            ))
            self.id = cursor.fetchone()[0]
            conn.commit()
            return self.id

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT gp.*, pt.ten_loai_gia, f.format_name 
            FROM global_price gp
            LEFT JOIN price_type pt ON gp.pricetype_id = pt.pricetype_id
            LEFT JOIN format f ON gp.format_id = f.format_id
            WHERE gp.active = TRUE
            ORDER BY gp.created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM global_price WHERE id = %s AND active = TRUE', (id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def get_by_format(format_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM global_price 
            WHERE format_id = %s AND active = TRUE
            ''', (format_id,))
            rows = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def update(id, data={}):
        with get_db_connection() as conn:
            cursor = conn.cursor()

            update_fields = []
            params = []

            for field, value in data.items():
                update_fields.append(f"{field} = %s")
                params.append(value)

            if update_fields:
                query = f'''
                UPDATE global_price 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND active = TRUE
                '''
                params.append(id)

                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE global_price SET active = FALSE WHERE id = %s
            ''', (id,))
            conn.commit()
