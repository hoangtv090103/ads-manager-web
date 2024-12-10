from configs.db import get_db_connection
class RemarketingSetting:
    def __init__(self, remarketing_id=None, ads_group_id=None,
                 auto_remarketing=False, tan_suat_hien_thi=0,
                 thoi_gian_giua_hai_lan_hien_thi=0, thoi_gian_remarketing=0,
                 stop_on_click=False, stop_on_view=False, max_view=0):
        self.remarketing_id = remarketing_id
        self.ads_group_id = ads_group_id
        self.auto_remarketing = auto_remarketing
        self.tan_suat_hien_thi = tan_suat_hien_thi
        self.thoi_gian_giua_hai_lan_hien_thi = thoi_gian_giua_hai_lan_hien_thi
        self.thoi_gian_remarketing = thoi_gian_remarketing
        self.stop_on_click = stop_on_click
        self.stop_on_view = stop_on_view
        self.max_view = max_view

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS remarketing_setting (
                remarketing_id SERIAL PRIMARY KEY,
                ads_group_id INTEGER NOT NULL,
                auto_remarketing BOOLEAN DEFAULT FALSE,
                tan_suat_hien_thi INTEGER,
                thoi_gian_giua_hai_lan_hien_thi INTEGER,
                thoi_gian_remarketing INTEGER,
                stop_on_click BOOLEAN DEFAULT FALSE,
                stop_on_view BOOLEAN DEFAULT FALSE,
                max_view INTEGER,
                FOREIGN KEY (ads_group_id) REFERENCES ads_group(ads_group_id)
                    ON DELETE CASCADE
            )
            ''')
            conn.commit() 
            
    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO remarketing_setting (
                ads_group_id, auto_remarketing, tan_suat_hien_thi, 
                thoi_gian_giua_hai_lan_hien_thi, thoi_gian_remarketing, 
                stop_on_click, stop_on_view, max_view
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ''', (
                self.ads_group_id, self.auto_remarketing, self.tan_suat_hien_thi,
                self.thoi_gian_giua_hai_lan_hien_thi, self.thoi_gian_remarketing,
                self.stop_on_click, self.stop_on_view, self.max_view
            ))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT 
                remarketing_id, 
                ads_group_id, 
                auto_remarketing, 
                tan_suat_hien_thi, 
                thoi_gian_giua_hai_lan_hien_thi, 
                thoi_gian_remarketing, 
                stop_on_click, 
                stop_on_view, 
                max_view, 
                created_at, 
                updated_at, 
                active 
            FROM remarketing_setting 
            ORDER BY created_at DESC
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
    def get_by_id(remarketing_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM remarketing_setting WHERE remarketing_id = %s', (remarketing_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    @staticmethod
    def update(remarketing_id, data={}):
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
                UPDATE remarketing_setting 
                SET {', '.join(update_fields)}
                WHERE remarketing_id = %s;
                '''
                params.append(remarketing_id)
                
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def delete_by_id(remarketing_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE remarketing_setting SET active = 0 WHERE remarketing_id = ?
            ''', (remarketing_id,))
            conn.commit()