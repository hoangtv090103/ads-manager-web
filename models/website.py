from configs.db import get_db_connection


class Website:
    def __init__(self, website_id=None, domain_website="", link_url="",
                 tong_so_luong_vung=0, publisher_id=None, webstatus_id=None,
                 active=True):
        self.website_id = website_id
        self.domain_website = domain_website
        self.link_url = link_url
        self.tong_so_luong_vung = tong_so_luong_vung
        self.publisher_id = publisher_id
        self.active = active

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS website (
                website_id SERIAL PRIMARY KEY,
                domain_website VARCHAR(255),
                link_url VARCHAR(255),
                tong_so_luong_vung INTEGER DEFAULT 0,
                publisher_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
                    ON DELETE SET NULL
            )
            ''')
            conn.commit()

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO website (domain_website, link_url, tong_so_luong_vung, publisher_id)
            VALUES (%s, %s, %s, %s)
            ''', (self.domain_website, self.link_url, self.tong_so_luong_vung, self.publisher_id))
            conn.commit()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT website_id, domain_website, link_url, tong_so_luong_vung, website.publisher_id, publisher.ten_publisher, publisher.email, website.created_at, website.updated_at, website.active 
            FROM website 
            LEFT JOIN publisher ON website.publisher_id = publisher.publisher_id
            WHERE website.active = true
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_all_has_price_list():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM website w
            LEFT JOIN website_price wp ON w.website_id = wp.website_id
            WHERE w.active = true AND wp.price_id IS NOT NULL
            ''')
            rows = cursor.fetchall()
            if not rows:
                return []
            return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    @staticmethod
    def get_by_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM website WHERE website_id = %s
            ''', (website_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(zip([column[0] for column in cursor.description], row))

    def update(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE website
            SET domain_website = %s, link_url = %s, tong_so_luong_vung = %s, publisher_id = %s
            WHERE website_id = %s
            ''', (self.domain_website, self.link_url, self.tong_so_luong_vung, self.publisher_id, self.website_id))
            conn.commit()

    @staticmethod
    def delete_by_id(website_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE website SET active = false WHERE website_id = %s
            ''', (website_id,))
            conn.commit()
