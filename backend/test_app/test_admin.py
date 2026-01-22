import pytest
from fastapi.testclient import TestClient
from main import app
import json
from admin.admin_crud import (
    get_all_admins,
    get_admin_by_id,
    get_admin_by_username
)
from database import LocalSession

client_401 = TestClient(app)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_admin():
    return {"username": "testadmin1", "password": "testpassword"}


def test_register_admin(client):
    data = {
        "username": "testadmin1",
        "password": "testpassword",
        "is_admin": True,
    }

    response = client.post("/spm/admin/register", json=data)
    assert response.status_code == 200


def test_admin_login_token(client, test_admin):
    """
    test admin login with token
    """
    response = client.post("/spm/admin/login", data=test_admin)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "username" in response.json()

    return response.json()["access_token"]


def test_delete_admin(client, test_admin):
    access_token = test_admin_login_token(client, test_admin)

    db = LocalSession()
    admin1 = get_admin_by_username(db, "testadmin1")

    response = client.delete(
        f"/spm/admin/{admin1.id}", 
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
