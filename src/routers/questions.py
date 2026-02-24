import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.question import SocraticQuestion
from src.models.definition import TaskDefinition
from src.schemas.question import QuestionResponse, AnswerRequest
from src.services.llm_service import llm_service

router = APIRouter(prefix="/api/v1/projects/{project_id}/questions", tags=["questions"])


@router.get("", response_model=list[QuestionResponse])
def list_questions(project_id: str, db: Session = Depends(get_db)):
    return db.query(SocraticQuestion).filter_by(project_id=project_id).order_by(SocraticQuestion.created_at).all()


@router.post("/generate", response_model=list[QuestionResponse])
def generate_questions(project_id: str, db: Session = Depends(get_db)):
    defn = db.query(TaskDefinition).filter_by(project_id=project_id).first()
    if not defn:
        raise HTTPException(400, "Task definition not found. Generate it first.")

    result = llm_service.generate(
        "socratic_questions.md",
        {
            "mission": defn.mission,
            "hard_constraints": json.dumps(defn.hard_constraints, ensure_ascii=False),
            "soft_objectives": json.dumps(defn.soft_objectives, ensure_ascii=False),
            "non_goals": json.dumps(defn.non_goals, ensure_ascii=False),
            "critical_metrics": json.dumps(defn.critical_metrics, ensure_ascii=False),
        },
    )

    # Clear old questions
    db.query(SocraticQuestion).filter_by(project_id=project_id).delete()

    questions = []
    for item in result:
        q = SocraticQuestion(
            project_id=project_id,
            category=item["category"],
            question=item["question"],
        )
        db.add(q)
        questions.append(q)

    db.commit()
    for q in questions:
        db.refresh(q)
    return questions


@router.post("/{question_id}/answer", response_model=QuestionResponse)
def answer_question(project_id: str, question_id: str, req: AnswerRequest, db: Session = Depends(get_db)):
    q = db.query(SocraticQuestion).filter_by(id=question_id, project_id=project_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    q.answer = req.answer
    db.commit()
    db.refresh(q)
    return q
