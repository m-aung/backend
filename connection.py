import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def shutdown_db_conn():
    """Dispose of the database engine to close all connections."""
    if 'engine' in globals() and engine:
        engine.dispose()
        print(f"Database connections for {env} environment disposed.")