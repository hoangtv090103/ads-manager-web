from configs.db import get_db_connection
class ProductGroupMapping:
    def __init__(self, mapping_id=None, product_id=None, productgroup_id=None):
        self.mapping_id = mapping_id
        self.product_id = product_id
        self.productgroup_id = productgroup_id

    @staticmethod
    def create_table():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_group_mapping (
                mapping_id SERIAL PRIMARY KEY,
                product_id INTEGER NOT NULL,
                productgroup_id INTEGER NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (product_id) REFERENCES product(product_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (productgroup_id) REFERENCES product_group(productgroup_id)
                    ON DELETE CASCADE,
                UNIQUE(product_id, productgroup_id)
            )
            ''')
            conn.commit() 