from src.models.definition import TaskDefinition
from src.models.alternative import Alternative
from src.models.must import MustEvaluation
from src.models.want import WantScore
from src.models.risk import Risk
from src.models.decision import DecisionRecord
from src.services.gate_service import check_gate_1, check_gate_2, check_gate_3


def test_gate_1_no_definition(db_session):
    result = check_gate_1(db_session, "fake-project")
    assert not result["overall_pass"]


def test_gate_1_pass(db_session):
    defn = TaskDefinition(
        project_id="p1",
        mission="Test mission",
        critical_metrics=[
            {"name": "M1", "target": "100", "method": "測試"},
            {"name": "M2", "target": "200", "method": "量測"},
            {"name": "M3", "target": "300", "method": "計算"},
        ],
    )
    db_session.add(defn)
    db_session.commit()

    result = check_gate_1(db_session, "p1")
    assert result["overall_pass"]


def test_gate_1_fail_missing_method(db_session):
    defn = TaskDefinition(
        project_id="p1",
        mission="Test",
        critical_metrics=[
            {"name": "M1", "target": "100", "method": "測試"},
            {"name": "M2", "target": "200", "method": ""},
            {"name": "M3", "target": "300", "method": "計算"},
        ],
    )
    db_session.add(defn)
    db_session.commit()

    result = check_gate_1(db_session, "p1")
    assert not result["overall_pass"]


def test_gate_2_pass(db_session):
    for i in range(3):
        alt = Alternative(
            project_id="p1", code=f"方案 {chr(65+i)}", name=f"Alt {i}",
            status="must_pass",
            mechanism={"p": "x"}, assumptions=["A1"], risks={"f": ["x"]},
        )
        db_session.add(alt)
    db_session.commit()

    result = check_gate_2(db_session, "p1")
    assert result["overall_pass"]


def test_gate_2_fail_too_few(db_session):
    alt = Alternative(
        project_id="p1", code="方案 A", name="Alt 0",
        status="must_pass",
        mechanism={"p": "x"}, assumptions=["A1"], risks={"f": ["x"]},
    )
    db_session.add(alt)
    db_session.commit()

    result = check_gate_2(db_session, "p1")
    assert not result["overall_pass"]


def test_gate_3_pass(db_session):
    dr = DecisionRecord(project_id="p1", statement="Test", signed_by="Alice")
    db_session.add(dr)
    db_session.commit()

    result = check_gate_3(db_session, "p1")
    assert result["overall_pass"]


def test_gate_3_fail_no_signoff(db_session):
    dr = DecisionRecord(project_id="p1", statement="Test")
    db_session.add(dr)
    db_session.commit()

    result = check_gate_3(db_session, "p1")
    assert not result["overall_pass"]
