"""API client for Streamlit to call FastAPI backend."""
import httpx

BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 300.0  # LLM calls can be slow (5 min for large generation)


def _url(path: str) -> str:
    return f"{BASE_URL}{path}"


def _handle(r: httpx.Response):
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        raise RuntimeError(f"API Error ({r.status_code}): {detail}")
    if r.headers.get("content-type", "").startswith("text/"):
        return r.text
    return r.json()


# --- Projects ---
def create_project(name: str, description: str = ""):
    return _handle(httpx.post(_url("/projects"), json={"name": name, "description": description}, timeout=TIMEOUT))

def list_projects():
    return _handle(httpx.get(_url("/projects"), timeout=TIMEOUT))

def get_project(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}"), timeout=TIMEOUT))

def update_project(pid: str, **kwargs):
    return _handle(httpx.put(_url(f"/projects/{pid}"), json=kwargs, timeout=TIMEOUT))


# --- Definitions ---
def get_definition(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/definitions"), timeout=TIMEOUT))

def generate_definition(pid: str, requirement_text: str, constraints: str = ""):
    return _handle(httpx.post(_url(f"/projects/{pid}/definitions/generate"), json={"requirement_text": requirement_text, "constraints": constraints}, timeout=TIMEOUT))

def update_definition(pid: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/definitions"), json=data, timeout=TIMEOUT))


# --- Questions ---
def list_questions(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/questions"), timeout=TIMEOUT))

def generate_questions(pid: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/questions/generate"), timeout=TIMEOUT))

def answer_question(pid: str, qid: str, answer: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/questions/{qid}/answer"), json={"answer": answer}, timeout=TIMEOUT))


# --- Contradictions ---
def list_contradictions(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/contradictions"), timeout=TIMEOUT))

def identify_contradictions(pid: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/contradictions/identify"), timeout=TIMEOUT))


# --- Causal Loops ---
def generate_causal_loops(pid: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/causal-loops/generate"), timeout=TIMEOUT))

def list_causal_loops(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/causal-loops"), timeout=TIMEOUT))

def create_causal_loop(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/causal-loops"), json=data, timeout=TIMEOUT))

def update_causal_loop(pid: str, loop_id: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/causal-loops/{loop_id}"), json=data, timeout=TIMEOUT))

def delete_causal_loop(pid: str, loop_id: str):
    return _handle(httpx.delete(_url(f"/projects/{pid}/causal-loops/{loop_id}"), timeout=TIMEOUT))


# --- Breakpoints ---
def list_breakpoints(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/breakpoints"), timeout=TIMEOUT))

def create_breakpoint(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/breakpoints"), json=data, timeout=TIMEOUT))

def update_breakpoint(pid: str, bp_id: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/breakpoints/{bp_id}"), json=data, timeout=TIMEOUT))

def delete_breakpoint(pid: str, bp_id: str):
    return _handle(httpx.delete(_url(f"/projects/{pid}/breakpoints/{bp_id}"), timeout=TIMEOUT))


# --- Unknown Factors ---
def list_unknown_factors(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/unknown-factors"), timeout=TIMEOUT))

def create_unknown_factor(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/unknown-factors"), json=data, timeout=TIMEOUT))

def update_unknown_factor(pid: str, uf_id: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/unknown-factors/{uf_id}"), json=data, timeout=TIMEOUT))

def delete_unknown_factor(pid: str, uf_id: str):
    return _handle(httpx.delete(_url(f"/projects/{pid}/unknown-factors/{uf_id}"), timeout=TIMEOUT))


# --- Assumptions ---
def list_assumptions(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/assumptions"), timeout=TIMEOUT))

def create_assumption(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/assumptions"), json=data, timeout=TIMEOUT))

def update_assumption(pid: str, aid: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/assumptions/{aid}"), json=data, timeout=TIMEOUT))

def extract_assumptions(pid: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/assumptions/extract"), timeout=TIMEOUT))

def disprove_assumption(pid: str, aid: str, reason: str):
    return _handle(httpx.post(
        _url(f"/projects/{pid}/assumptions/{aid}/disprove"),
        json={"reason": reason}, timeout=TIMEOUT))


# --- TRIZ ---
def list_triz(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/triz"), timeout=TIMEOUT))

def solve_triz(pid: str, contradiction_id: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/triz/solve"), json={"contradiction_id": contradiction_id}, timeout=TIMEOUT))

def get_triz_result(pid: str, contradiction_id: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/triz/result/{contradiction_id}"), timeout=TIMEOUT))

def generate_triz(pid: str, contradiction_id: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/triz/generate"), json={"contradiction_id": contradiction_id}, timeout=TIMEOUT))


# --- SCAMPER ---
def list_scamper(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/scamper"), timeout=TIMEOUT))

def generate_scamper(pid: str, subsystem: str, constraints: str = ""):
    return _handle(httpx.post(_url(f"/projects/{pid}/scamper/generate"), json={"subsystem": subsystem, "constraints": constraints}, timeout=TIMEOUT))


# --- Alternatives ---
def list_alternatives(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/alternatives"), timeout=TIMEOUT))

def generate_alternatives(pid: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/alternatives/generate"), timeout=TIMEOUT))

def update_alternative(pid: str, alt_id: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/alternatives/{alt_id}"), json=data, timeout=TIMEOUT))


# --- MUST ---
def list_must(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/must"), timeout=TIMEOUT))

def evaluate_must(pid: str, alternative_id: str, results: dict, notes: str = ""):
    return _handle(httpx.post(_url(f"/projects/{pid}/must/evaluate"), json={"alternative_id": alternative_id, "results": results, "notes": notes}, timeout=TIMEOUT))


# --- WANT ---
def list_want_criteria(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/want/criteria"), timeout=TIMEOUT))

def create_want_criteria(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/want/criteria"), json=data, timeout=TIMEOUT))

def list_want_scores(pid: str, alternative_id: str | None = None):
    params = {"alternative_id": alternative_id} if alternative_id else {}
    return _handle(httpx.get(_url(f"/projects/{pid}/want/scores"), params=params, timeout=TIMEOUT))

def score_want(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/want/scores"), json=data, timeout=TIMEOUT))

def get_want_totals(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/want/totals"), timeout=TIMEOUT))


# --- Risks ---
def list_risks(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/risks"), timeout=TIMEOUT))

def create_risk(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/risks"), json=data, timeout=TIMEOUT))

def update_risk(pid: str, rid: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/risks/{rid}"), json=data, timeout=TIMEOUT))


# --- Experiments ---
def list_experiments(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/experiments"), timeout=TIMEOUT))

def create_experiment(pid: str, data: dict):
    return _handle(httpx.post(_url(f"/projects/{pid}/experiments"), json=data, timeout=TIMEOUT))

def update_experiment(pid: str, eid: str, data: dict):
    return _handle(httpx.put(_url(f"/projects/{pid}/experiments/{eid}"), json=data, timeout=TIMEOUT))


# --- Decisions ---
def get_decision(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/decisions"), timeout=TIMEOUT))

def generate_decision(pid: str):
    return _handle(httpx.post(_url(f"/projects/{pid}/decisions/generate"), timeout=TIMEOUT))

def signoff_decision(pid: str, signed_by: str):
    return _handle(httpx.put(_url(f"/projects/{pid}/decisions/signoff"), json={"signed_by": signed_by}, timeout=TIMEOUT))


# --- Gates ---
def check_gate(pid: str, gate_number: int):
    return _handle(httpx.post(_url(f"/projects/{pid}/gates/{gate_number}/check"), timeout=TIMEOUT))

def list_gates(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/gates"), timeout=TIMEOUT))


# --- Export ---
def export_markdown(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/export/markdown"), timeout=TIMEOUT))

def export_json(pid: str):
    return _handle(httpx.get(_url(f"/projects/{pid}/export/json"), timeout=TIMEOUT))
