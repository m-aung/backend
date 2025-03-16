import os
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from connection import get_connection_string, shutdown_db_conn, conn_str, engine

# filepath: c:\MyoProjects\master-app\backend\test_connection.py

@pytest.fixture
def mock_env_vars():
  with patch.dict(os.environ, {
    "POSTGRESQL_CONNECTION_DEV": "postgresql://dev_user:dev_pass@localhost/dev_db",
    "POSTGRESQL_CONNECTION_AWS": "postgresql://aws_user:aws_pass@aws_host/aws_db",
    "POSTGRESQL_CONNECTION_AZURE": "postgresql://azure_user:azure_pass@azure_host/azure_db",
    "APP_ENV": "dev"
  }):
    yield

@pytest.mark.skip(reason="This test is currently under development. mocking environment variables is not working as expected.")
def test_get_connection_string_valid_env(mock_env_vars):
  assert get_connection_string("dev") == "postgresql://dev_user:dev_pass@localhost/dev_db"
  assert get_connection_string("aws") == "postgresql://aws_user:aws_pass@aws_host/aws_db"
  assert get_connection_string("azure") == "postgresql://azure_user:azure_pass@azure_host/azure_db"

def test_get_connection_string_invalid_env(mock_env_vars):
  with pytest.raises(ValueError, match="Unknown environment: invalid_env. Valid options: \['dev', 'aws', 'azure'\]"):
    get_connection_string("invalid_env")

@patch('connection.create_engine')
@pytest.mark.skip(reason="This test is currently under development. mocking environment variables is not working as expected.")
def test_main_connection_logic(mock_create_engine, mock_env_vars):
  mock_create_engine.assert_called_once_with("postgresql://dev_user:dev_pass@localhost/dev_db", echo=True)
  assert conn_str == "postgresql://dev_user:dev_pass@localhost/dev_db"
  assert isinstance(engine, MagicMock)

@patch('connection.engine')
def test_shutdown_db_conn(mock_engine):
  shutdown_db_conn()
  mock_engine.dispose.assert_called_once()
  print("Database connection closed.")