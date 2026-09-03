import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_url = os.getenv("DIRECT_URL")

    if not database_url:
        raise ValueError("DIRECT_URL is not set in .env")

    return psycopg2.connect(database_url)