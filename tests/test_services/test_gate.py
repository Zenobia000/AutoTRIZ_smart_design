from src.models.definition import TaskDefinition
from src.models.alternative import Alternative
from src.models.assumption import Assumption
from src.models.contradiction import Contradiction
from src.models.causal_loop import CausalLoop, Breakpoint
from src.models.experiment import Experiment
from src.models.pre_cad_review import PreCadReview
from src.models.risk import Risk
from src.models.decision import DecisionRecord
from src.services.gate_service import (
    check_gate_1_1, check_gate_1_2, check_gate_1_3,
    check_gate_2_1, check_gate_2_2, check_gate_2_3,
    check_gate_3_2, check_gate_3_3,
)


PID = "test-project"


# --- Gate 1.1 ---

def test_gate_1_1_no_definition(db_session):
    result = check_gate_1_1(db_session, PID)
    assert not result["overall_pass"]


def test_gate_1_1_pass(db_session):
    defn = TaskDefinition(
        project_id=PID,
        mission="Test mission",
        critical_metrics=[
            {"name": "M1", "target": "100", "method": "test"},
            {"name": "M2", "target": "200", "method": "sim"},
            {"name": "M3", "target": "300", "method": "calc"},
        ],
    )
    db_session.add(defn)
    db_session.commit()
    result = check_gate_1_1(db_session, PID)
    assert result["overall_pass"]


def test_gate_1_1_fail_missing_method(db_session):
    defn = TaskDefinition(
        project_id=PID,
        mission="Test",
        critical_metrics=[
            {"name": "M1", "target": "100", "method": "test"},
            {"name": "M2", "target": "200", "method": ""},
            {"name": "M3", "target": "300", "method": "calc"},
        ],
    )
    db_session.add(defn)
    db_session.commit()
    result = check_gate_1_1(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 1.2 ---

def _seed_assumptions(db_session, count=10):
    for i in range(count):
        db_session.add(Assumption(
            project_id=PID, code=f"A{i+1}", content=f"Assumption {i+1}",
            risk_level="High" if i < 3 else "Medium",
        ))
    db_session.commit()


def test_gate_1_2_pass(db_session):
    _seed_assumptions(db_session, 10)
    for i in range(3):
        db_session.add(Contradiction(
            project_id=PID, code=f"C{i+1}",
            improve_param=f"P{i}", worsen_param=f"P{i+1}", engineering_desc=f"Desc {i}",
        ))
    db_session.commit()
    result = check_gate_1_2(db_session, PID)
    assert result["overall_pass"]


def test_gate_1_2_fail_too_few_assumptions(db_session):
    _seed_assumptions(db_session, 5)
    for i in range(3):
        db_session.add(Contradiction(
            project_id=PID, code=f"C{i+1}",
            improve_param=f"P{i}", worsen_param=f"P{i+1}", engineering_desc=f"Desc {i}",
        ))
    db_session.commit()
    result = check_gate_1_2(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 1.3 ---

def test_gate_1_3_pass(db_session):
    loop = CausalLoop(project_id=PID, name="Loop1", nodes=["A", "B"])
    db_session.add(loop)
    db_session.flush()
    for i in range(3):
        db_session.add(Breakpoint(project_id=PID, causal_loop_id=loop.id, code=f"BP-{i:03d}", location=f"Loc{i}", description=f"BP{i}"))
    db_session.add(Contradiction(
        project_id=PID, code="C1",
        improve_param="P1", worsen_param="P2", engineering_desc="Desc",
        contradiction_types=["technical"],
    ))
    db_session.commit()
    result = check_gate_1_3(db_session, PID)
    assert result["overall_pass"]


def test_gate_1_3_fail_no_loop(db_session):
    for i in range(3):
        db_session.add(Breakpoint(project_id=PID, code=f"BP-{i:03d}", location=f"Loc{i}", description=f"BP{i}"))
    db_session.commit()
    result = check_gate_1_3(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 2.1 ---

def test_gate_2_1_pass(db_session):
    for i in range(3):
        a = Assumption(project_id=PID, code=f"A{i+1}", content=f"High risk {i}", risk_level="High")
        db_session.add(a)
        db_session.flush()
        db_session.add(Experiment(
            project_id=PID, goal=f"Verify A{i+1}", question=f"Q{i}", method=f"M{i}",
            assumption_id=a.id,
        ))
    db_session.commit()
    result = check_gate_2_1(db_session, PID)
    assert result["overall_pass"]


def test_gate_2_1_fail_no_experiment(db_session):
    for i in range(3):
        db_session.add(Assumption(project_id=PID, code=f"A{i+1}", content=f"High risk {i}", risk_level="High"))
    db_session.commit()
    result = check_gate_2_1(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 2.2 ---

def test_gate_2_2_pass(db_session):
    for i in range(3):
        db_session.add(Alternative(
            project_id=PID, code=f"Alt {chr(65+i)}", name=f"Alt {i}",
            status="must_pass", mechanism={"p": "x"}, assumptions=["A1"], risks={"f": ["x"]},
        ))
    db_session.commit()
    result = check_gate_2_2(db_session, PID)
    assert result["overall_pass"]


def test_gate_2_2_fail_too_few(db_session):
    db_session.add(Alternative(
        project_id=PID, code="Alt A", name="Alt 0",
        status="must_pass", mechanism={"p": "x"}, assumptions=["A1"], risks={"f": ["x"]},
    ))
    db_session.commit()
    result = check_gate_2_2(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 2.3 ---

def test_gate_2_3_pass(db_session):
    for i in range(3):
        alt = Alternative(
            project_id=PID, code=f"Alt {chr(65+i)}", name=f"Alt {i}",
            status="selected", robust_scores={"score": 80},
        )
        db_session.add(alt)
        db_session.flush()
        db_session.add(PreCadReview(
            project_id=PID, alternative_id=alt.id,
            space_score=4, cost_score=3, safety_score=5, decoupling_score=3, supply_score=4,
            overall_pass=True, reviewer="Tester",
        ))
    db_session.commit()
    result = check_gate_2_3(db_session, PID)
    assert result["overall_pass"]


def test_gate_2_3_fail_no_review(db_session):
    for i in range(3):
        db_session.add(Alternative(
            project_id=PID, code=f"Alt {chr(65+i)}", name=f"Alt {i}",
            status="selected", robust_scores={"score": 80},
        ))
    db_session.commit()
    result = check_gate_2_3(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 3.2 ---

def test_gate_3_2_pass(db_session):
    dr = DecisionRecord(project_id=PID, statement="Test", signed_by="Alice")
    db_session.add(dr)
    db_session.commit()
    result = check_gate_3_2(db_session, PID)
    assert result["overall_pass"]


def test_gate_3_2_fail_no_signoff(db_session):
    dr = DecisionRecord(project_id=PID, statement="Test")
    db_session.add(dr)
    db_session.commit()
    result = check_gate_3_2(db_session, PID)
    assert not result["overall_pass"]


# --- Gate 3.3 ---

def test_gate_3_3_pass(db_session):
    dr = DecisionRecord(
        project_id=PID, statement="Final", signed_by="Alice",
        action_items=[{"task": "T1", "owner": "Bob", "due": "2025-01-01"}],
    )
    db_session.add(dr)
    # All H risks have mitigation
    db_session.add(Risk(
        project_id=PID, description="Overheat", risk_type="technical",
        probability="H", severity="H", level="H*", mitigation="Add heatsink",
    ))
    db_session.commit()
    result = check_gate_3_3(db_session, PID)
    assert result["overall_pass"]


def test_gate_3_3_fail_no_mitigation(db_session):
    dr = DecisionRecord(
        project_id=PID, statement="Final", signed_by="Alice",
        action_items=[{"task": "T1", "owner": "Bob", "due": "2025-01-01"}],
    )
    db_session.add(dr)
    db_session.add(Risk(
        project_id=PID, description="Overheat", risk_type="technical",
        probability="H", severity="H", level="H*", mitigation="",
    ))
    db_session.commit()
    result = check_gate_3_3(db_session, PID)
    assert not result["overall_pass"]
