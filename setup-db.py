import os
import re
from sqlalchemy import create_engine, text

ENV_CONNECTIONS = {
    "dev": os.environ.get("POSTGRESQL_CONNECTION_DEV"),
    "aws": os.environ.get("POSTGRESQL_CONNECTION_AWS"),
    "azure": os.environ.get("POSTGRESQL_CONNECTION_AZURE")
}

def get_connection_string(env: str) -> str:
    try:
        return ENV_CONNECTIONS[env]
    except KeyError:
        raise ValueError(f"Unknown environment: {env}. Valid options: {list(ENV_CONNECTIONS.keys())}")

# Determine the target environment from the environment variable.
env = os.environ.get("APP_ENV", "dev")
conn_str = get_connection_string(env)
print(f"Connecting to {env} environment with: {conn_str}")

# Create SQLAlchemy engine.
engine = create_engine(conn_str, echo=True)

def execute_schema_from_file(filepath: str):
    """Reads and executes the SQL schema from a given file."""
    with open(filepath, 'r') as file:
        sql = file.read()

    # Split the SQL script into individual statements using semicolons.
    statements = [stmt.strip() for stmt in re.split(r';\s*', sql) if stmt.strip()]

    with engine.begin() as connection:
        for stmt in statements:
            print(f"Executing: {stmt.splitlines()[0]} ...")
            connection.execute(text(stmt))

if __name__ == "__main__":
    execute_schema_from_file("./database/create-tables.sql")
    print("Database schema setup complete.")
