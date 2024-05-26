import sys
import os
import logging
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db.database import connect_db

def fetch_data(sql_file):
    try:
        # Open and read the SQL file
        with open(sql_file, "r") as file:
            sql_queries = file.read()
        
        # Connect to the database and fetch data
        conn = connect_db()
        all_data = pd.read_sql(sql_queries, conn)
        conn.close()
        
        logging.info('Data fetched successfully')
        return all_data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None
