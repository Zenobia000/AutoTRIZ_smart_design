"""Test Pre-CAD Review CRUD."""


def test_create_pre_cad_pass(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={"code": "Alt A", "name": "Alt A"})
    alt_id = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/pre-cad-reviews", json={
        "alternative_id": alt_id,
        "space_score": 4, "space_note": "OK",
        "cost_score": 3, "cost_note": "Tight",
        "safety_score": 5, "safety_note": "Good",
        "decoupling_score": 3, "decoupling_note": "Acceptable",
        "supply_score": 4, "supply_note": "Dual source",
        "reviewer": "Tester",
    })
    assert r.status_code == 200
    assert r.json()["overall_pass"] is True


def test_create_pre_cad_fail(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={"code": "Alt A", "name": "Alt A"})
    alt_id = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/pre-cad-reviews", json={
        "alternative_id": alt_id,
        "space_score": 2, "cost_score": 3, "safety_score": 5,
        "decoupling_score": 3, "supply_score": 4,
        "reviewer": "Tester",
    })
    assert r.status_code == 200
    assert r.json()["overall_pass"] is False


def test_update_recalc(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={"code": "Alt A", "name": "Alt A"})
    alt_id = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/pre-cad-reviews", json={
        "alternative_id": alt_id,
        "space_score": 2, "cost_score": 3, "safety_score": 5,
        "decoupling_score": 3, "supply_score": 4,
        "reviewer": "Tester",
    })
    rid = r.json()["id"]
    assert r.json()["overall_pass"] is False

    # Fix the space_score
    r = client.put(f"/api/v1/projects/{pid}/pre-cad-reviews/{rid}", json={"space_score": 4})
    assert r.status_code == 200
    assert r.json()["overall_pass"] is True


def test_list_and_delete(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={"code": "Alt A", "name": "Alt A"})
    alt_id = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/pre-cad-reviews", json={
        "alternative_id": alt_id,
        "space_score": 3, "cost_score": 3, "safety_score": 3,
        "decoupling_score": 3, "supply_score": 3,
        "reviewer": "Tester",
    })
    rid = r.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/pre-cad-reviews")
    assert len(r.json()) == 1

    r = client.delete(f"/api/v1/projects/{pid}/pre-cad-reviews/{rid}")
    assert r.status_code == 200

    r = client.get(f"/api/v1/projects/{pid}/pre-cad-reviews")
    assert len(r.json()) == 0
