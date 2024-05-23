import os
import argparse
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.database import databaseConnect, databaseDisconnect


def migration_down():
    schemas = ["raw", "dbo"]
    conn = databaseConnect()
    cur = conn.cursor()
    for schema in schemas:
        cur.execute(
            f""" 
        DROP SCHEMA IF EXISTS {schema} CASCADE;
        """
        )
    print("[+] VyagutaInfo Database cleaned!\n")
    conn.commit()
    databaseDisconnect(conn, cur)


def migration_up():
    conn = databaseConnect()
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
                        print(f"[+] Executed {filename}\n")
                    except Exception as e:
                        conn.rollback()
                        print(f"[-] Failed to execute {filename}: ", e)
    databaseDisconnect(conn, cur)


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
