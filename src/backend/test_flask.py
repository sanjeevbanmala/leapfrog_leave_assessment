import os
import sys
import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from httpx import AsyncClient

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)
from backend.main import app, get_leave_info, run_insert_leave_info


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"success": True}


@patch("backend.main.get_leave_info")
@pytest.mark.asyncio
async def test_leave_info(mock_get_leave_info, client):
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
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/leave_info")
        assert response.status_code == 200
        assert response.json() == {
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
