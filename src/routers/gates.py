from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.gate import GateCheck
from src.schemas.gate import GateCheckResponse
from src.services import gate_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/gates", tags=["gates"])

VALID_GATES = {"1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.2", "3.3"}

CHECKERS = {
    "1.1": gate_service.check_gate_1_1,
    "1.2": gate_service.check_gate_1_2,
    "1.3": gate_service.check_gate_1_3,
    "2.1": gate_service.check_gate_2_1,
    "2.2": gate_service.check_gate_2_2,
    "2.3": gate_service.check_gate_2_3,
    "3.2": gate_service.check_gate_3_2,
    "3.3": gate_service.check_gate_3_3,
}


@router.post("/{gate_id}/check", response_model=GateCheckResponse)
def check_gate(project_id: str, gate_id: str, db: Session = Depends(get_db)):
    if gate_id not in VALID_GATES:
        raise HTTPException(400, f"Gate ID must be one of {sorted(VALID_GATES)}")

    result = CHECKERS[gate_id](db, project_id)

    gate = GateCheck(
        project_id=project_id,
        gate_id=gate_id,
        checklist=result["checklist"],
        overall_pass=result["overall_pass"],
    )
    db.add(gate)
    db.commit()
    db.refresh(gate)
    return gate


@router.get("", response_model=list[GateCheckResponse])
def list_gates(project_id: str, db: Session = Depends(get_db)):
    return db.query(GateCheck).filter_by(project_id=project_id).order_by(GateCheck.gate_id).all()
