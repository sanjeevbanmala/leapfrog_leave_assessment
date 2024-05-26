import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.main import app, get_leave_info, insert_data


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"success": True}


@patch("backend.main.get_leave_info")
def test_leave_info(mock_get_leave_info, client):
    mock_get_leave_info.return_value = {
        "data": [
            {
                "id": 1,
                "userId": 123,
                "empId": "EMP001",
                "startDate": "2024-05-01",
                "endDate": "2024-05-05",
            }
        ]
    }
    response = client.get("/leave_info")
    assert response.status_code == 200
    assert response.json == {
        "data": [
            {
                "id": 1,
                "userId": 123,
                "empId": "EMP001",
                "startDate": "2024-05-01",
                "endDate": "2024-05-05",
            }
        ]
    }


@patch("backend.main.connect_db")
@patch("backend.main.close_db")
@patch("backend.main.requests.get")
def test_insert_data(mock_requests_get, mock_close_db, mock_connect_db, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": 1,
                "userId": 123,
                "empId": "EMP001",
                "startDate": "2024-05-01",
                "endDate": "2024-05-05",
            }
        ]
    }
    mock_requests_get.return_value = mock_response
    response = client.get("/insert_leave_info")
    assert response.status_code == 200
    assert response.json == {"success": "Leave Data Inserted Successfully!"}
