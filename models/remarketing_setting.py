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