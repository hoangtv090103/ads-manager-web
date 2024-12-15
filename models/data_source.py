from configs.db import get_db_connection
from datetime import datetime


class DataSource:
    def __init__(self, source_id=None, ten_nguon_du_lieu=None, duong_dan_file=None, user_id=None,
                 status_id=None, so_san_pham_dung=0, so_san_pham_loi=0,
                 created_at=None, updated_at=None):
        self.source_id = source_id
        self.ten_nguon_du_lieu = ten_nguon_du_lieu
        self.duong_dan_file = duong_dan_file
        self.user_id = user_id
        self.status_id = status_id
        self.so_san_pham_dung = so_san_pham_dung
        self.so_san_pham_loi = so_san_pham_loi
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_source (
                    source_id SERIAL PRIMARY KEY,
                    ten_nguon_du_lieu VARCHAR(255) NOT NULL,
                    duong_dan_file VARCHAR(255),
                    user_id INTEGER REFERENCES users(user_id),
                    status_id INTEGER REFERENCES source_status(source_status_id),
                    so_san_pham_dung INTEGER DEFAULT 0,
                    so_san_pham_loi INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO data_source (
                    ten_nguon_du_lieu, duong_dan_file, user_id, status_id, 
                    so_san_pham_dung, so_san_pham_loi
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING source_id
                ''', (
                    self.ten_nguon_du_lieu, self.duong_dan_file, self.user_id,
                    self.status_id, self.so_san_pham_dung, self.so_san_pham_loi
                ))
                source_id = cursor.fetchone()[0]
                conn.commit()
                return source_id
        except Exception as e:
            print(f"Error saving data source: {str(e)}")
            raise

    @staticmethod
    def get_all():
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT ds.source_id, ds.ten_nguon_du_lieu, ds.duong_dan_file, 
                           ds.status_id, ds.so_san_pham_dung, ds.so_san_pham_loi, 
                           ds.created_at, ds.updated_at,
                           u.username, ss.ten_trang_thai,
                           COUNT(p.product_id) as total_products
                    FROM data_source ds
                    LEFT JOIN users u ON ds.user_id = u.user_id
                    LEFT JOIN source_status ss ON ds.status_id = ss.source_status_id
                    LEFT JOIN product p ON ds.source_id = p.source_id AND p.active = true
                    GROUP BY ds.source_id, u.username, ss.ten_trang_thai
                    ORDER BY ds.created_at DESC
                ''')
                rows = cursor.fetchall()
                if not rows:
                    return []
                return [dict(zip([column[0] for column in cursor.description], row))
                        for row in rows]
        except Exception as e:
            print(f"Error getting all data sources: {str(e)}")
            raise

    def update(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE data_source 
                SET ten_nguon_du_lieu = %s,
                    duong_dan_file = %s,
                    status_id = %s,
                    so_san_pham_dung = %s,
                    so_san_pham_loi = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE source_id = %s
                ''', (
                    self.ten_nguon_du_lieu, self.duong_dan_file,
                    self.status_id, self.so_san_pham_dung,
                    self.so_san_pham_loi, self.source_id
                ))
                conn.commit()
        except Exception as e:
            print(f"Error updating data source: {str(e)}")
            raise

    @staticmethod
    def get_by_id(source_id):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT ds.*, u.username, ss.ten_trang_thai,
                           COUNT(p.product_id) as total_products
                    FROM data_source ds
                    LEFT JOIN users u ON ds.user_id = u.user_id
                    LEFT JOIN source_status ss ON ds.status_id = ss.source_status_id
                    LEFT JOIN product p ON ds.source_id = p.source_id AND p.active = true
                    WHERE ds.source_id = %s
                    GROUP BY ds.source_id, u.username, ss.ten_trang_thai
                ''', (source_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                return dict(zip([column[0] for column in cursor.description], row))
        except Exception as e:
            print(f"Error getting data source by ID: {str(e)}")
            raise

    @staticmethod
    def get_status_id(status_name):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT source_status_id FROM source_status 
                    WHERE ten_trang_thai = %s
                ''', (status_name,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Error getting status ID: {str(e)}")
            raise

    @staticmethod
    def update_source_status(source_id, status_name):
        try:
            status_id = DataSource.get_status_id(status_name)
            if status_id is None:
                raise ValueError(f"Status not found: {status_name}")

            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE data_source 
                    SET status_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE source_id = %s
                ''', (status_id, source_id))
                conn.commit()
        except Exception as e:
            print(f"Error updating source status: {str(e)}")
            raise

    @staticmethod
    def update_source_products(source_id, valid_count, error_count):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE data_source 
                    SET so_san_pham_dung = %s, 
                        so_san_pham_loi = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE source_id = %s    
                ''', (valid_count, error_count, source_id))
                conn.commit()
        except Exception as e:
            print(f"Error updating source products: {str(e)}")
            raise

    @staticmethod
    def delete(source_id):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # First deactivate all products associated with this source
                cursor.execute('''
                    UPDATE product 
                    SET active = false,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE source_id = %s
                ''', (source_id,))
                
                # Then delete the data source
                cursor.execute('''
                    DELETE FROM data_source 
                    WHERE source_id = %s
                ''', (source_id,))
                conn.commit()
        except Exception as e:
            print(f"Error deleting data source: {str(e)}")
            raise
