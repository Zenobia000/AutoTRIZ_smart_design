"""Integration tests for assumption batch extraction endpoint."""
from unittest.mock import patch


def _setup_project_with_upstream(client):
    """Helper: create project + task definition + contradiction + return pid."""
    r = client.post("/api/v1/projects", json={"name": "HDA Test"})
    pid = r.json()["id"]

    # Task definition (PUT creates or updates)
    client.put(f"/api/v1/projects/{pid}/definitions", json={
        "mission": "Design a lightweight bracket",
        "hard_constraints": [{"name": "Max weight", "value": "500g", "source": "spec"}],
        "soft_objectives": [],
        "non_goals": [],
        "critical_metrics": [],
    })

    # Contradiction
    client.post(f"/api/v1/projects/{pid}/contradictions", json={
        "code": "C1",
        "improve_param": "strength",
        "worsen_param": "weight",
        "engineering_desc": "Thicker wall increases strength but adds weight",
        "physical_contradiction": "Wall must be thick and thin",
        "source": "constraint",
    })

    return pid


MOCK_EXTRACT_RESULT = [
    {
        "content": "Bracket material yield strength >= 350 MPa at operating temp",
        "assumption_type": "可靠度/壽命",
        "worst_consequence": "Structural failure under load",
        "risk_level": "High",
        "verification_method": "Material cert + tensile test at 85C",
        "acceptance_criteria": "Yield strength >= 350 MPa at 85C",
        "source_refs": [
            {"type": "task_definition", "code": "TD"},
            {"type": "contradiction", "code": "C1"},
        ],
    },
    {
        "content": "Wall thickness 2mm achievable with die casting",
        "assumption_type": "製程/DFM",
        "worst_consequence": "Part not manufacturable, redesign needed",
        "risk_level": "Medium",
        "verification_method": "DFM review with supplier",
        "acceptance_criteria": "Supplier confirms feasibility",
        "source_refs": [
            {"type": "contradiction", "code": "C1"},
        ],
    },
]


def _mock_generate(template_name, variables):
    if "assumption_extract" in template_name:
        return MOCK_EXTRACT_RESULT
    return []


@patch("src.routers.assumptions.llm_service.generate", side_effect=_mock_generate)
def test_extract_assumptions(mock_llm, client):
    """POST /assumptions/extract returns extracted assumptions."""
    pid = _setup_project_with_upstream(client)

    r = client.post(f"/api/v1/projects/{pid}/assumptions/extract")
    assert r.status_code == 200
    data = r.json()

    assert data["extracted_count"] == 2
    assert len(data["assumptions"]) == 2
    assert data["assumptions"][0]["code"] == "A-001"
    assert data["assumptions"][1]["code"] == "A-002"
    assert data["assumptions"][0]["source"] == "AI 萃取"
    assert len(data["assumptions"][0]["source_refs"]) == 2
    assert data["assumptions"][0]["risk_level"] == "High"

    # Verify persisted in DB
    r = client.get(f"/api/v1/projects/{pid}/assumptions")
    assert len(r.json()) == 2


@patch("src.routers.assumptions.llm_service.generate", side_effect=_mock_generate)
def test_extract_preserves_manual(mock_llm, client):
    """Manual assumptions survive AI extraction."""
    pid = _setup_project_with_upstream(client)

    # Create a manual assumption first
    client.post(f"/api/v1/projects/{pid}/assumptions", json={
        "code": "A-001",
        "content": "Manual assumption about thermal expansion",
        "source": "工程常識",
    })

    r = client.post(f"/api/v1/projects/{pid}/assumptions/extract")
    assert r.status_code == 200

    # Should have manual + 2 AI-extracted
    r = client.get(f"/api/v1/projects/{pid}/assumptions")
    all_assumptions = r.json()
    assert len(all_assumptions) == 3

    manual = [a for a in all_assumptions if a["source"] != "AI 萃取"]
    ai = [a for a in all_assumptions if a["source"] == "AI 萃取"]
    assert len(manual) == 1
    assert len(ai) == 2
    assert manual[0]["content"] == "Manual assumption about thermal expansion"
    # AI assumptions numbered after manual
    assert ai[0]["code"] == "A-002"
    assert ai[1]["code"] == "A-003"


def test_extract_no_definition(client):
    """POST /assumptions/extract without task definition returns 400."""
    r = client.post("/api/v1/projects", json={"name": "Empty"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/assumptions/extract")
    assert r.status_code == 400


@patch("src.routers.assumptions.llm_service.generate", side_effect=_mock_generate)
def test_extract_re_extract_replaces_ai(mock_llm, client):
    """Re-extracting replaces old AI assumptions, keeps manual."""
    pid = _setup_project_with_upstream(client)

    # Manual assumption
    client.post(f"/api/v1/projects/{pid}/assumptions", json={
        "code": "A-001",
        "content": "Manual one",
        "source": "規格需求",
    })

    # First extraction
    client.post(f"/api/v1/projects/{pid}/assumptions/extract")
    r = client.get(f"/api/v1/projects/{pid}/assumptions")
    assert len(r.json()) == 3  # 1 manual + 2 AI

    # Second extraction — should replace AI, keep manual
    client.post(f"/api/v1/projects/{pid}/assumptions/extract")
    r = client.get(f"/api/v1/projects/{pid}/assumptions")
    all_a = r.json()
    assert len(all_a) == 3  # still 1 manual + 2 AI (not 5)

    manual = [a for a in all_a if a["source"] != "AI 萃取"]
    assert len(manual) == 1
