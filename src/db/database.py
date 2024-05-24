import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("SERVER", "localhost")
DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("USERNAME", "sa")
PASSWORD = os.getenv("PASSWORD")


def databaseConnect():
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
        print(f"[-] Exception Occured: ", e)


def databaseDisconnect(connection, cursor):
    """
    This function helps to disconnect from database.
    """
    try:
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"[-] Exception Occured: ", e)
