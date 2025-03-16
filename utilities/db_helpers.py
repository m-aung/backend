
import re
from sqlalchemy import  text ,Engine

def execute_schema_from_file(engine:Engine, filepath: str):
    """Reads and executes the SQL schema from a given file."""
    with open(filepath, 'r') as file:
        sql = file.read()

    # Split the SQL script into individual statements using semicolons.
    statements = [stmt.strip() for stmt in re.split(r';\s*', sql) if stmt.strip()]

    with engine.begin() as connection:
        for stmt in statements:
            print(f"Executing: {stmt.splitlines()[0]} ...")
            connection.execute(text(stmt))