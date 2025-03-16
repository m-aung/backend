import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

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

def shutdown_db_conn():
    """Close database all connections."""
    engine.dispose()
    print("Database connection closed.")