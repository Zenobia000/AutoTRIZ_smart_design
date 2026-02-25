"""Tests for assumption disprove endpoint and unknown factor assumption_refs."""


def _create_project(client):
    r = client.post("/api/v1/projects", json={"name": "PDCA Test"})
    return r.json()["id"]


def _create_assumption(client, pid, code="A-001", source_refs=None):
    return client.post(f"/api/v1/projects/{pid}/assumptions", json={
        "code": code,
        "content": f"Test assumption {code}",
        "source_refs": source_refs or [],
    }).json()


def test_disprove_assumption(client):
    """POST /assumptions/{id}/disprove sets status and records reason."""
    pid = _create_project(client)
    a = _create_assumption(client, pid)

    r = client.post(f"/api/v1/projects/{pid}/assumptions/{a['id']}/disprove",
                    json={"reason": "Test failed at 85C"})
    assert r.status_code == 200
    data = r.json()

    assert data["assumption"]["status"] == "Disproved"
    assert data["assumption"]["disproved_reason"] == "Test failed at 85C"
    assert data["assumption"]["disproved_at"] is not None
    assert isinstance(data["impact_analysis"], list)
    assert isinstance(data["recommended_actions"], list)

    # Verify persisted
    r = client.get(f"/api/v1/projects/{pid}/assumptions")
    a_list = r.json()
    assert a_list[0]["status"] == "Disproved"
    assert a_list[0]["disproved_reason"] == "Test failed at 85C"


def test_disprove_with_impact(client):
    """Disprove assumption linked to contradiction returns impact analysis."""
    pid = _create_project(client)

    # Create contradiction
    r = client.post(f"/api/v1/projects/{pid}/contradictions", json={
        "code": "C1",
        "improve_param": "strength",
        "worsen_param": "weight",
        "engineering_desc": "Thicker wall adds weight",
        "source": "test",
    })
    cid = r.json()["id"]

    # Create assumption with source_refs pointing to contradiction
    a = _create_assumption(client, pid, source_refs=[
        {"type": "contradiction", "code": "C1", "id": cid},
    ])

    r = client.post(f"/api/v1/projects/{pid}/assumptions/{a['id']}/disprove",
                    json={"reason": "Material yield too low"})
    assert r.status_code == 200
    data = r.json()

    # Should find the contradiction in impact
    types = [item["type"] for item in data["impact_analysis"]]
    assert "contradiction" in types
    assert any("C1" in action for action in data["recommended_actions"])


def test_disprove_not_found(client):
    """POST /assumptions/bad-id/disprove returns 404."""
    pid = _create_project(client)
    r = client.post(f"/api/v1/projects/{pid}/assumptions/nonexistent/disprove",
                    json={"reason": "test"})
    assert r.status_code == 404


def test_disprove_already_disproved(client):
    """POST /disprove on already-disproved assumption returns 400."""
    pid = _create_project(client)
    a = _create_assumption(client, pid)

    # First disprove
    r = client.post(f"/api/v1/projects/{pid}/assumptions/{a['id']}/disprove",
                    json={"reason": "First reason"})
    assert r.status_code == 200

    # Second disprove
    r = client.post(f"/api/v1/projects/{pid}/assumptions/{a['id']}/disprove",
                    json={"reason": "Second reason"})
    assert r.status_code == 400


# --- Unknown Factor assumption_refs tests ---

def test_create_unknown_factor_with_assumption_refs(client):
    """Create unknown factor with structured assumption_refs."""
    pid = _create_project(client)
    a = _create_assumption(client, pid)

    r = client.post(f"/api/v1/projects/{pid}/unknown-factors", json={
        "code": "U-001",
        "name": "Temperature variation",
        "category": "環境",
        "levels": ["25C", "55C", "85C"],
        "assumption_refs": [{"assumption_id": a["id"], "code": "A-001"}],
    })
    assert r.status_code == 200
    data = r.json()
    assert len(data["assumption_refs"]) == 1
    assert data["assumption_refs"][0]["code"] == "A-001"
    assert data["assumption_refs"][0]["assumption_id"] == a["id"]


def test_update_unknown_factor_assumption_refs(client):
    """Update assumption_refs on unknown factor."""
    pid = _create_project(client)
    a1 = _create_assumption(client, pid, code="A-001")
    a2 = _create_assumption(client, pid, code="A-002")

    # Create with one ref
    r = client.post(f"/api/v1/projects/{pid}/unknown-factors", json={
        "code": "U-001",
        "name": "Load variation",
        "assumption_refs": [{"assumption_id": a1["id"], "code": "A-001"}],
    })
    uf_id = r.json()["id"]

    # Update to two refs
    r = client.put(f"/api/v1/projects/{pid}/unknown-factors/{uf_id}", json={
        "assumption_refs": [
            {"assumption_id": a1["id"], "code": "A-001"},
            {"assumption_id": a2["id"], "code": "A-002"},
        ],
    })
    assert r.status_code == 200
    assert len(r.json()["assumption_refs"]) == 2
