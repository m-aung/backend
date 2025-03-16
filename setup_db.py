from connection import  shutdown_db_conn
from utilities.db_helpers import execute_schema_from_file

if __name__ == "__main__":
    try:
        execute_schema_from_file("./database/create-tables.sql")
        print("Database schema setup complete.")
    finally:
        shutdown_db_conn()
