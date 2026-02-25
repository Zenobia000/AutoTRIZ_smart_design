from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.gate import GateCheck
from src.schemas.gate import GateCheckResponse
from src.services import gate_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/gates", tags=["gates"])


@router.post("/{gate_number}/check", response_model=GateCheckResponse)
def check_gate(project_id: str, gate_number: int, db: Session = Depends(get_db)):
    if gate_number not in (1, 2, 3):
        raise HTTPException(400, "Gate number must be 1, 2, or 3")

    checkers = {
        1: gate_service.check_gate_1,
        2: gate_service.check_gate_2,
        3: gate_service.check_gate_3,
    }

    result = checkers[gate_number](db, project_id)

    gate = GateCheck(
        project_id=project_id,
        gate_number=gate_number,
        checklist=result["checklist"],
        overall_pass=result["overall_pass"],
    )
    db.add(gate)
    db.commit()
    db.refresh(gate)
    return gate


@router.get("", response_model=list[GateCheckResponse])
def list_gates(project_id: str, db: Session = Depends(get_db)):
    return db.query(GateCheck).filter_by(project_id=project_id).order_by(GateCheck.gate_number).all()
