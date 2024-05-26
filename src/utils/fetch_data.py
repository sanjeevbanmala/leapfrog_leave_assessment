import sys
import os
import pandas as pd
from utils.database import connect_db
from utils.logging import get_logger

logger = get_logger()


def fetch_data(sql_file):
    try:
        # Open and read the SQL file
        with open(sql_file, "r") as file:
            sql_queries = file.read()

        # Connect to the database and fetch data
        conn = connect_db()
        all_data = pd.read_sql(sql_queries, conn)
        conn.close()

        logger.info("Data fetched successfully")
        return all_data
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None
