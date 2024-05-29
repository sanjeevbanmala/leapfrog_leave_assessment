import os
import asyncpg
import psycopg2

from dotenv import load_dotenv
from utils.logging import get_logger

logger = get_logger()

load_dotenv()

SERVER = os.getenv("SERVER", "localhost")
DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("USERNAME", "sa")
PASSWORD = os.getenv("PASSWORD")


async def connect_db():
    try:
        connection = await asyncpg.connect(
            user=USERNAME,
            password=PASSWORD,
            host=SERVER,
            port=5432,
            database=DATABASE,
        )
        return connection
    except Exception as e:
        logger.error(f"[-] Exception Occured: ", e)


def sync_connect_db():
    try:
        connection = psycopg2.connect(
            user=USERNAME,
            password=PASSWORD,
            host=SERVER,
            port=5432,
            database=DATABASE,
        )
        return connection
    except Exception as e:
        logger.error(f"[-] Exception Occured: ", e)


def close_db(connection, cursor):
    """
    This function helps to disconnect from database.
    """
    try:
        cursor.close()
        connection.close()
    except Exception as e:
        logger.error(f"[-] Exception Occured: ", e)
