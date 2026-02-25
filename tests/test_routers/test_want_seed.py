"""Test WANT criteria seed endpoint."""


def test_seed_creates_6(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/want/criteria/seed")
    assert r.status_code == 200
    criteria = r.json()
    assert len(criteria) == 6
    codes = {c["code"] for c in criteria}
    assert codes == {"W1", "W2", "W3", "W4", "W5", "W6"}


def test_seed_409_if_exists(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    # First seed — OK
    r = client.post(f"/api/v1/projects/{pid}/want/criteria/seed")
    assert r.status_code == 200

    # Second seed — 409
    r = client.post(f"/api/v1/projects/{pid}/want/criteria/seed")
    assert r.status_code == 409
