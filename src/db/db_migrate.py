import os
import argparse
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.database import connect_db, close_db
from utils.logging import get_logger

logger = get_logger()


def migration_down():
    schemas = ["raw", "dbo"]
    conn = connect_db()
    cur = conn.cursor()
    for schema in schemas:
        cur.execute(
            f""" 
        DROP SCHEMA IF EXISTS {schema} CASCADE;
        """
        )
    logger.info("[+] VyagutaInfo Database cleaned!\n")
    print("[+] VyagutaInfo Database cleaned!\n")
    conn.commit()
    close_db(conn, cur)


def migration_up():
    conn = connect_db()
    cur = conn.cursor()
    directories = ["./sql/migrations", "./sql/procedures"]
    for directory in directories:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".sql"):
                with open(os.path.join(directory, filename), "r") as f:
                    sql_command = f.read()
                    try:
                        cur.execute(sql_command)
                        conn.commit()
                        logger.info(f"[+] Executed {filename}\n")
                        print(f"[+] Executed {filename}\n")
                    except Exception as e:
                        conn.rollback()
                        logger.error(f"[-] Failed to execute {filename}: ", e)
    close_db(conn, cur)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--up",
        action="store_true",
        help="Run migration_up for Vyaguta Leave Info tables.",
    )
    parser.add_argument(
        "--down",
        action="store_true",
        help="Run migration_down for Vyaguta Leave Info tables.",
    )
    args = parser.parse_args()

    if args.up:
        migration_up()
    elif args.down:
        migration_down()
