import os
import pytest
from unittest.mock import patch, MagicMock
from db_migrate import migration_up, migration_down


# Mocking database functions
@patch("db_migrate.connect_db")
@patch("db_migrate.close_db")
def test_migration_up(mock_close_db, mock_connect_db):
    # Mocking cursor and execute methods
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    # Mocking os.listdir
    with patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ["file1.sql", "file2.sql"]
        migration_up()
        # Assert that the cursor.execute is called twice for each file
        assert mock_cursor.execute.call_count == 2 * 2  # 2 files * 2 directories
        # Assert that the logger.info is called for each file
        assert mock_conn.commit.call_count == 2  # 2 directories


# Similar test for migration_down
@patch("db_migrate.connect_db")
@patch("db_migrate.close_db")
def test_migration_down(mock_close_db, mock_connect_db):
    # Mocking cursor and execute methods
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    migration_down()
    assert mock_cursor.execute.call_count == 2  # 2 schemas
    assert mock_conn.commit.call_count == 1
