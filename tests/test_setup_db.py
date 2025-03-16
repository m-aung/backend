import pytest
from unittest.mock import patch, MagicMock

@patch("setup_db.execute_schema_from_file")
@patch("setup_db.shutdown_db_conn")
@pytest.mark.skip(reason="This test is currently under development.")
def test_setup_db(mock_shutdown_db_conn, mock_execute_schema_from_file):
    # Mock the execute_schema_from_file function
    mock_execute_schema_from_file.return_value = None

    # Mock the shutdown_db_conn function
    mock_shutdown_db_conn.return_value = None

    # Import the setup_db script to trigger the execution
    import setup_db

    # Check if the execute_schema_from_file function was called with the correct argument
    mock_execute_schema_from_file.assert_called_once_with("./database/create-tables.sql")

    # Check if the shutdown_db_conn function was called
    mock_shutdown_db_conn.assert_called_once()

if __name__ == "__main__":
    pytest.main()