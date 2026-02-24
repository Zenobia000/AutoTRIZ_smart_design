"""Test Phase I-III CRUD flows (no LLM)."""


def test_definition_crud(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    # PUT definition
    defn = {
        "mission": "Test mission",
        "hard_constraints": [{"name": "HC1", "value": "100", "source": "spec"}],
        "soft_objectives": [{"name": "SO1", "direction": "越高越好"}],
        "non_goals": ["NG1", "NG2"],
        "critical_metrics": [
            {"name": "CM1", "target": "100", "method": "test"},
            {"name": "CM2", "target": "200", "method": "sim"},
            {"name": "CM3", "target": "300", "method": "calc"},
        ],
    }
    r = client.put(f"/api/v1/projects/{pid}/definitions", json=defn)
    assert r.status_code == 200
    assert r.json()["mission"] == "Test mission"

    # GET
    r = client.get(f"/api/v1/projects/{pid}/definitions")
    assert r.status_code == 200
    assert r.json()["mission"] == "Test mission"


def test_assumption_crud(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/assumptions", json={
        "code": "A1", "content": "假設1", "source": "推測"
    })
    assert r.status_code == 200
    aid = r.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/assumptions")
    assert len(r.json()) == 1

    r = client.put(f"/api/v1/projects/{pid}/assumptions/{aid}", json={"status": "verified"})
    assert r.json()["status"] == "verified"


def test_alternative_crud(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={
        "code": "方案 A", "name": "Alt A"
    })
    assert r.status_code == 200
    assert r.json()["status"] == "candidate"


def test_must_evaluation(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={"code": "方案 A", "name": "Alt A"})
    alt_id = r.json()["id"]

    # Pass
    r = client.post(f"/api/v1/projects/{pid}/must/evaluate", json={
        "alternative_id": alt_id, "results": {"M1": True, "M2": True}
    })
    assert r.status_code == 200
    assert r.json()["overall_pass"] is True

    # Fail
    r = client.post(f"/api/v1/projects/{pid}/must/evaluate", json={
        "alternative_id": alt_id, "results": {"M1": True, "M2": False}
    })
    assert r.json()["overall_pass"] is False


def test_want_scoring(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    # Create criteria
    r = client.post(f"/api/v1/projects/{pid}/want/criteria", json={
        "code": "W1", "name": "效率", "weight": 8
    })
    cid = r.json()["id"]

    # Create alternative
    r = client.post(f"/api/v1/projects/{pid}/alternatives", json={"code": "方案 A", "name": "Alt A"})
    alt_id = r.json()["id"]

    # Score
    r = client.post(f"/api/v1/projects/{pid}/want/scores", json={
        "alternative_id": alt_id, "criteria_id": cid, "score": 7, "evidence": "計算書"
    })
    assert r.status_code == 200
    assert r.json()["weighted_score"] == 56  # 8 × 7


def test_risk_creation(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/risks", json={
        "description": "散熱不足", "risk_type": "technical",
        "probability": "H", "severity": "H"
    })
    assert r.status_code == 200
    assert r.json()["level"] == "H*"


def test_experiment_crud(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/experiments", json={
        "goal": "驗證散熱", "question": "溫升是否<40K?", "method": "模擬"
    })
    assert r.status_code == 200
    eid = r.json()["id"]

    r = client.put(f"/api/v1/projects/{pid}/experiments/{eid}", json={"status": "completed", "result": "通過"})
    assert r.json()["status"] == "completed"


def test_gate_1_check(client):
    r = client.post("/api/v1/projects", json={"name": "Test"})
    pid = r.json()["id"]

    # Without definition — should fail
    r = client.post(f"/api/v1/projects/{pid}/gates/1/check")
    assert r.status_code == 200
    assert r.json()["overall_pass"] is False

    # Add definition
    client.put(f"/api/v1/projects/{pid}/definitions", json={
        "mission": "Test", "hard_constraints": [], "soft_objectives": [],
        "non_goals": [], "critical_metrics": [
            {"name": "M1", "target": "100", "method": "test"},
            {"name": "M2", "target": "200", "method": "sim"},
            {"name": "M3", "target": "300", "method": "calc"},
        ],
    })
    r = client.post(f"/api/v1/projects/{pid}/gates/1/check")
    assert r.json()["overall_pass"] is True


def test_export_markdown(client):
    r = client.post("/api/v1/projects", json={"name": "Export Test"})
    pid = r.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/export/markdown")
    assert r.status_code == 200
    assert "Export Test" in r.text


def test_export_json(client):
    r = client.post("/api/v1/projects", json={"name": "Export Test"})
    pid = r.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/export/json")
    assert r.status_code == 200
    assert r.json()["project"]["name"] == "Export Test"
