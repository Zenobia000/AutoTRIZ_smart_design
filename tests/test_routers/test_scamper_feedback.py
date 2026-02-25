"""Tests for SCAMPER new contradictions feedback + subsystem suggestions."""


def _create_project(client):
    r = client.post("/api/v1/projects", json={"name": "SCAMPER Test"})
    return r.json()["id"]


def _create_contradiction(client, pid, code="C1"):
    return client.post(f"/api/v1/projects/{pid}/contradictions", json={
        "code": code,
        "improve_param": "strength",
        "worsen_param": "weight",
        "engineering_desc": f"Test contradiction {code}",
        "source": "test",
    }).json()


def _create_breakpoint(client, pid, code="BP-001", location="馬達-減速機界面"):
    return client.post(f"/api/v1/projects/{pid}/breakpoints", json={
        "code": code,
        "location": location,
        "description": "Test breakpoint",
    }).json()


def _create_scamper_with_contradictions(client, pid):
    """Directly create a ScamperVariant via the DB to avoid LLM dependency."""
    from src.models.scamper import ScamperVariant
    from src.database import get_db
    from src.main import app

    db = next(app.dependency_overrides[get_db]())
    v = ScamperVariant(
        project_id=pid,
        subsystem="散熱系統",
        action="S",
        target="散熱片材料",
        mechanism="銅替換鋁",
        failure_mode="成本上升",
        supply_risk="銅價波動",
        assumptions="A-001",
        verification="熱阻測試",
        new_contradictions=[
            {
                "improve": "散熱效率",
                "worsen": "重量",
                "engineering_desc": "銅散熱片重量增加 50%",
            },
            {
                "improve": "導熱係數",
                "worsen": "成本",
                "engineering_desc": "銅材料成本增加 3x",
            },
        ],
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


# --- new_contradictions field tests ---

def test_scamper_new_contradictions_field(client):
    """ScamperVariant should persist new_contradictions JSON."""
    pid = _create_project(client)
    _create_scamper_with_contradictions(client, pid)

    r = client.get(f"/api/v1/projects/{pid}/scamper")
    assert r.status_code == 200
    variants = r.json()
    assert len(variants) == 1
    assert len(variants[0]["new_contradictions"]) == 2
    assert variants[0]["new_contradictions"][0]["improve"] == "散熱效率"


# --- feedback-contradictions tests ---

def test_feedback_contradictions(client):
    """POST /feedback-contradictions creates new Contradiction records."""
    pid = _create_project(client)
    _create_scamper_with_contradictions(client, pid)

    r = client.post(f"/api/v1/projects/{pid}/scamper/feedback-contradictions")
    assert r.status_code == 200
    data = r.json()
    assert data["created_count"] == 2
    assert len(data["contradictions"]) == 2

    # Verify contradictions exist
    r = client.get(f"/api/v1/projects/{pid}/contradictions")
    assert len(r.json()) == 2


def test_feedback_dedup(client):
    """Feedback should not create duplicate contradictions."""
    pid = _create_project(client)

    # Pre-create a contradiction with same desc
    _create_contradiction(client, pid, code="C1")

    _create_scamper_with_contradictions(client, pid)

    # Add a SCAMPER variant with contradiction matching existing
    from src.models.scamper import ScamperVariant
    from src.database import get_db
    from src.main import app
    db = next(app.dependency_overrides[get_db]())
    v = ScamperVariant(
        project_id=pid, subsystem="X", action="C", target="Y",
        mechanism="Z", new_contradictions=[
            {"improve": "a", "worsen": "b", "engineering_desc": "Test contradiction C1"},
        ],
    )
    db.add(v)
    db.commit()

    r = client.post(f"/api/v1/projects/{pid}/scamper/feedback-contradictions")
    data = r.json()
    # Should only create 2 (from the first variant), not the dup
    assert data["created_count"] == 2

    r = client.get(f"/api/v1/projects/{pid}/contradictions")
    # 1 pre-existing + 2 new = 3
    assert len(r.json()) == 3


def test_feedback_empty(client):
    """Feedback with no new contradictions returns 0."""
    pid = _create_project(client)
    r = client.post(f"/api/v1/projects/{pid}/scamper/feedback-contradictions")
    assert r.status_code == 200
    assert r.json()["created_count"] == 0


# --- subsystem-suggestions tests ---

def test_subsystem_suggestions_from_breakpoints(client):
    """GET /subsystem-suggestions returns breakpoint locations."""
    pid = _create_project(client)
    _create_breakpoint(client, pid, "BP-001", "馬達-減速機界面")
    _create_breakpoint(client, pid, "BP-002", "控制器散熱模組")

    r = client.get(f"/api/v1/projects/{pid}/scamper/subsystem-suggestions")
    assert r.status_code == 200
    suggestions = r.json()
    assert "馬達-減速機界面" in suggestions
    assert "控制器散熱模組" in suggestions


def test_subsystem_suggestions_empty(client):
    """No breakpoints → empty suggestions."""
    pid = _create_project(client)
    r = client.get(f"/api/v1/projects/{pid}/scamper/subsystem-suggestions")
    assert r.status_code == 200
    assert r.json() == []
