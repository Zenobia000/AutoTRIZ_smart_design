"""Tests for Anti-Anchor Sprint endpoint."""


def _create_project(client):
    r = client.post("/api/v1/projects", json={"name": "AA Test"})
    return r.json()["id"]


def _create_contradiction(client, pid, code="C1"):
    return client.post(f"/api/v1/projects/{pid}/contradictions", json={
        "code": code,
        "improve_param": "speed",
        "worsen_param": "noise",
        "engineering_desc": "Higher speed increases NVH",
        "source": "test",
    }).json()


def test_anti_anchor_requires_contradictions(client):
    """POST /anti-anchor without contradictions returns 400."""
    pid = _create_project(client)
    r = client.post(f"/api/v1/projects/{pid}/alternatives/anti-anchor")
    assert r.status_code == 400
    assert "contradictions" in r.json()["detail"].lower()


def test_anti_anchor_endpoint_exists(client):
    """POST /anti-anchor with contradictions reaches the handler (not 404/405).

    Without LLM API key, the endpoint raises RuntimeError from llm_service.
    TestClient raises server exceptions by default, so we catch it to confirm
    the route exists and reaches the LLM call (past all validation).
    """
    pid = _create_project(client)
    _create_contradiction(client, pid, "C1")

    try:
        r = client.post(f"/api/v1/projects/{pid}/alternatives/anti-anchor")
        # If LLM is available, should return 200
        assert r.status_code == 200
    except RuntimeError as e:
        # LLM unavailable — proves route exists and reached LLM call
        assert "LLM generation failed" in str(e)


def test_anti_anchor_alternatives_status(client):
    """Anti-anchor alternatives should have status='anti_anchor'."""
    from src.models.alternative import Alternative
    from src.database import get_db
    from src.main import app

    pid = _create_project(client)
    _create_contradiction(client, pid)

    # Directly create anti_anchor alternatives to test status filtering
    db = next(app.dependency_overrides[get_db]())
    for i in range(3):
        a = Alternative(
            project_id=pid,
            code=f"AA-{i+1}",
            name=f"Anti-Anchor Concept {i+1}",
            source="Anti-Anchor Sprint",
            status="anti_anchor",
        )
        db.add(a)
    db.commit()

    r = client.get(f"/api/v1/projects/{pid}/alternatives")
    assert r.status_code == 200
    alts = r.json()
    aa = [a for a in alts if a["status"] == "anti_anchor"]
    assert len(aa) == 3
    assert all(a["source"] == "Anti-Anchor Sprint" for a in aa)
