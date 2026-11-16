from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/v2/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_get_profile():
    r = client.post("/api/v2/profile", json={"name": "Jiya", "age": 20, "state": "Rajasthan"})
    assert r.status_code == 201
    pid = r.json()["id"]
    g = client.get(f"/api/v2/profile/{pid}")
    assert g.status_code == 200
    assert g.json()["name"] == "Jiya"


def test_update_profile():
    pid = client.post("/api/v2/profile", json={"name": "A"}).json()["id"]
    u = client.put(f"/api/v2/profile/{pid}", json={"name": "B", "age": 22})
    assert u.status_code == 200
    assert u.json()["name"] == "B"
    assert client.put("/api/v2/profile/nope", json={"name": "X"}).status_code == 404


def test_scheme_search_and_detail():
    s = client.get("/api/v2/schemes", params={"q": "kisan"})
    assert s.status_code == 200
    assert s.json()["count"] == 1
    assert client.get("/api/v2/schemes/edu-001").status_code == 200
    assert client.get("/api/v2/schemes/xyz").status_code == 404
