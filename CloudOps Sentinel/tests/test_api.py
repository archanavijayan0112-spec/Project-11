from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_resources_endpoint_returns_inventory():
    response = client.get("/resources")
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) >= 1
    assert {"id", "name", "type", "region", "state", "cost_per_hour_usd"} <= set(body["items"][0])


def test_create_incident():
    response = client.post(
        "/incidents",
        json={"title": "Database latency spike", "severity": "high", "resource_id": "rds-main-001"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Database latency spike"
    assert body["severity"] == "high"
    assert body["resource_id"] == "rds-main-001"
    assert "id" in body


def test_metrics_endpoint_is_prometheus_text():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "cloudops_resources_total" in response.text
    assert response.headers["content-type"].startswith("text/plain")

