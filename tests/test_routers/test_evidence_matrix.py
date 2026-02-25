"""Test Evidence Matrix aggregation endpoint."""


def test_evidence_matrix_aggregation(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    # Create assumption
    r = client.post(f"/api/v1/projects/{pid}/assumptions", json={
        "code": "A1", "content": "Material holds", "source": "estimate", "risk_level": "High",
    })
    aid = r.json()["id"]

    # Create experiments linked to assumption
    client.post(f"/api/v1/projects/{pid}/experiments", json={
        "goal": "Sim test", "question": "Does it hold?", "method": "FEA",
        "assumption_id": aid, "evidence_level": "E2",
    })
    client.post(f"/api/v1/projects/{pid}/experiments", json={
        "goal": "Proto test", "question": "Real check", "method": "physical",
        "assumption_id": aid, "evidence_level": "E3",
    })

    r = client.get(f"/api/v1/projects/{pid}/experiments/evidence-matrix")
    assert r.status_code == 200
    matrix = r.json()["matrix"]
    assert len(matrix) == 1
    assert matrix[0]["assumption_code"] == "A1"
    assert matrix[0]["best_evidence_level"] == "E3"
    assert matrix[0]["experiment_count"] == 2


def test_evidence_matrix_empty(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/experiments/evidence-matrix")
    assert r.status_code == 200
    assert r.json()["matrix"] == []
