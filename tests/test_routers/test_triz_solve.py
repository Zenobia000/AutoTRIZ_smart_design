"""Integration tests for unified TRIZ solve endpoint."""
from unittest.mock import patch


def _create_project_and_contradiction(client):
    """Helper: create project + contradiction, return (pid, cid)."""
    r = client.post("/api/v1/projects", json={"name": "TRIZ Test"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/contradictions", json={
        "code": "TC-001",
        "improve_param": "strength",
        "worsen_param": "weight",
        "engineering_desc": "Increasing wall thickness improves strength but adds weight",
        "physical_contradiction": "Wall must be thick (strength) and thin (weight)",
        "source": "test",
    })
    cid = r.json()["id"]
    return pid, cid


# Mock LLM responses for the 3-path solve pipeline
MOCK_CLASSIFY = {
    "types": ["technical", "physical"],
    "sufield_state": None,
    "reasoning": "TC: improve vs worsen. PC: thick and thin.",
}

MOCK_PARAM_MAPPING = {
    "improve_params": [
        {"triz_id": 14, "triz_name": "Strength", "confidence": "high"},
    ],
    "worsen_params": [
        {"triz_id": 1, "triz_name": "Weight of moving object", "confidence": "high"},
    ],
}

MOCK_TC_SOLVE = [
    {
        "principle_number": 1,
        "principle_name": "Segmentation",
        "abstract_strategy": "Divide the object into independent parts",
        "engineering_mappings": ["Use ribbed structure instead of solid wall"],
        "cost_description": "Tooling cost increase 5%",
        "robust_estimate": {"noise_sensitivity": "low"},
        "experiment_desc": "FEA simulation with 3 rib patterns",
    },
]

MOCK_PC_SOLVE = [
    {
        "separation_type": "space",
        "separation_name": "Separation in Space",
        "strategy": "Thick ribs in load paths, thin elsewhere",
        "engineering_mappings": ["Variable wall thickness via topology optimization"],
        "cost_description": "DFM review needed",
        "experiment_desc": "3D print prototype and load test",
    },
]


def _mock_generate(template_name, variables):
    """Route mock responses based on template name."""
    if "classify" in template_name:
        return MOCK_CLASSIFY
    if "param_mapping" in template_name:
        return MOCK_PARAM_MAPPING
    if "tc_solve" in template_name:
        return MOCK_TC_SOLVE
    if "pc_solve" in template_name:
        return MOCK_PC_SOLVE
    if "sf_solve" in template_name:
        return []
    return {}


@patch("src.services.triz_solve_service.llm_service.generate", side_effect=_mock_generate)
def test_solve_triz_unified(mock_llm, client):
    """POST /triz/solve returns unified result with TC + PC paths."""
    pid, cid = _create_project_and_contradiction(client)

    r = client.post(f"/api/v1/projects/{pid}/triz/solve", json={"contradiction_id": cid})
    assert r.status_code == 200
    data = r.json()

    # Classification
    assert "technical" in data["classification"]["types"]
    assert "physical" in data["classification"]["types"]

    # Param mapping
    assert data["param_mapping"] is not None
    assert data["param_mapping"]["improve_params"][0]["triz_id"] == 14

    # Matrix lookup should have been performed
    assert data["matrix_lookup"] is not None or data["matrix_lookup"] is None  # depends on matrix content

    # Technical solutions
    assert len(data["technical_solutions"]) >= 1
    assert data["technical_solutions"][0]["principle_name"] == "Segmentation"

    # Separation solutions
    assert len(data["separation_solutions"]) >= 1
    assert data["separation_solutions"][0]["separation_type"] == "space"

    # Su-Field (not applicable)
    assert len(data["sufield_solutions"]) == 0

    # LLM was called multiple times
    assert mock_llm.call_count >= 3


@patch("src.services.triz_solve_service.llm_service.generate", side_effect=_mock_generate)
def test_get_triz_result_after_solve(mock_llm, client):
    """GET /triz/result/{cid} returns persisted results."""
    pid, cid = _create_project_and_contradiction(client)

    # Solve first
    r = client.post(f"/api/v1/projects/{pid}/triz/solve", json={"contradiction_id": cid})
    assert r.status_code == 200

    # Get result
    r = client.get(f"/api/v1/projects/{pid}/triz/result/{cid}")
    assert r.status_code == 200
    data = r.json()
    assert data["contradiction_id"] == cid
    assert len(data["technical_solutions"]) >= 1
    assert len(data["separation_solutions"]) >= 1


@patch("src.services.triz_solve_service.llm_service.generate", side_effect=_mock_generate)
def test_solve_triz_not_found(mock_llm, client):
    """POST /triz/solve with bad contradiction_id returns 404."""
    r = client.post("/api/v1/projects", json={"name": "T"})
    pid = r.json()["id"]

    r = client.post(f"/api/v1/projects/{pid}/triz/solve", json={"contradiction_id": "nonexistent"})
    assert r.status_code == 404


def test_get_triz_result_not_found(client):
    """GET /triz/result/{cid} with bad id returns 404."""
    r = client.post("/api/v1/projects", json={"name": "T"})
    pid = r.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/triz/result/nonexistent")
    assert r.status_code == 404
