import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RD Design Copilot",
    version="0.5.0",
    description="AI-assisted early concept design system MVP",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {type(exc).__name__}: {exc}")
    return JSONResponse(status_code=500, content={"detail": f"{type(exc).__name__}: {exc}"})


@app.get("/health")
def health():
    return {"status": "ok"}


# Phase 1: Define routers
from src.routers import projects, definitions, questions, contradictions, causal_loops, gates

app.include_router(projects.router)
app.include_router(definitions.router)
app.include_router(questions.router)
app.include_router(contradictions.router)
app.include_router(causal_loops.router)
app.include_router(gates.router)

# Phase 2: Diverge routers
from src.routers import assumptions, unknown_factors, triz, scamper, alternatives, must, pre_cad_reviews

app.include_router(assumptions.router)
app.include_router(unknown_factors.router)
app.include_router(triz.router)
app.include_router(scamper.router)
app.include_router(alternatives.router)
app.include_router(must.router)
app.include_router(pre_cad_reviews.router)

# Phase 3: Converge routers
from src.routers import want, risks, experiments, decisions, export

app.include_router(want.router)
app.include_router(risks.router)
app.include_router(experiments.router)
app.include_router(decisions.router)
app.include_router(export.router)
