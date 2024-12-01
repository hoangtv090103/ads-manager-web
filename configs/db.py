import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        cursor_factory=DictCursor
    )
