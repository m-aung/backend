import pytest
from unittest.mock import patch, mock_open, MagicMock
from sqlalchemy.sql import text
from sqlalchemy.engine import Engine
from utilities.db_helpers import execute_schema_from_file

@patch("builtins.open", new_callable=mock_open, read_data="CREATE TABLE test (id INT PRIMARY KEY);\nINSERT INTO test (id) VALUES (1);")
@patch("sqlalchemy.engine.Engine.begin")
@pytest.mark.skip(reason="This test is currently under development.")
def test_execute_schema_from_file(mock_engine_begin, mock_file):
    mock_connection = MagicMock()
    mock_engine_begin.return_value.__enter__.return_value = mock_connection

    # Create a mock engine
    mock_engine = MagicMock(spec=Engine)
    mock_engine.begin.return_value.__enter__.return_value = mock_connection

    execute_schema_from_file(mock_engine, "dummy_path.sql")

    # Check if the file was opened
    mock_file.assert_called_once_with("dummy_path.sql", 'r')

    # Check if the SQL statements were executed
    expected_statements = [
        text("CREATE TABLE test (id INT PRIMARY KEY)"),
        text("INSERT INTO test (id) VALUES (1)")
    ]
    for stmt in expected_statements:
        mock_connection.execute.assert_any_call(stmt)

    # Check if the connection was closed
    mock_connection.__exit__.assert_called_once()

if __name__ == "__main__":
    pytest.main()