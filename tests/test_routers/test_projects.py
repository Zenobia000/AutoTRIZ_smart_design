def test_create_project(client):
    r = client.post("/api/v1/projects", json={"name": "Test Project", "description": "desc"})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Test Project"
    assert data["status"] == "DRAFT"


def test_list_projects(client):
    client.post("/api/v1/projects", json={"name": "P1"})
    client.post("/api/v1/projects", json={"name": "P2"})
    r = client.get("/api/v1/projects")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_project(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]
    r = client.get(f"/api/v1/projects/{pid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Test"


def test_update_project(client):
    r = client.post("/api/v1/projects", json={"name": "Old"})
    pid = r.json()["id"]
    r = client.put(f"/api/v1/projects/{pid}", json={"name": "New"})
    assert r.json()["name"] == "New"


def test_state_transition_valid(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]
    r = client.put(f"/api/v1/projects/{pid}", json={"status": "PHASE_I"})
    assert r.status_code == 200
    assert r.json()["status"] == "PHASE_I"


def test_state_transition_invalid(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]
    r = client.put(f"/api/v1/projects/{pid}", json={"status": "PHASE_III"})
    assert r.status_code == 400


def test_delete_project(client):
    r = client.post("/api/v1/projects", json={"name": "ToDelete"})
    pid = r.json()["id"]
    r = client.delete(f"/api/v1/projects/{pid}")
    assert r.status_code == 200
    r = client.get(f"/api/v1/projects/{pid}")
    assert r.status_code == 404
