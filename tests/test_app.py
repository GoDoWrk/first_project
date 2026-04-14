import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def set_test_db(tmp_path):
    os.environ["DATABASE_PATH"] = str(tmp_path / "test.db")


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_service_and_render() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/services",
            data={
                "name": "Proxmox",
                "url": "https://proxmox.local",
                "description": "Hypervisor",
                "status_enabled": "on",
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert "Proxmox" in response.text
    assert "https://proxmox.local" in response.text


def test_notes_update() -> None:
    with TestClient(app) as client:
        client.post("/notes", data={"content": "Buy spare SD card"}, follow_redirects=True)
        response = client.get("/")

    assert response.status_code == 200
    assert "Buy spare SD card" in response.text
