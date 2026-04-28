from fastapi import FastAPI

from app.schemas.lead_schema import LeadAnalysisResponse, LeadRequest
from app.services.lead_service import analyze_lead


app = FastAPI(
    title="AI Lead Form Analyzer API",
    description=(
        "Analyze incoming lead form submissions and return a structured "
        "lead quality assessment."
    ),
    version="0.1.0",
)


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "AI Lead Form Analyzer API is running."}


@app.post(
    "/analyze-lead",
    response_model=LeadAnalysisResponse,
    tags=["Lead Analysis"],
    summary="Analyze an incoming lead",
)
def analyze_lead_endpoint(payload: LeadRequest) -> LeadAnalysisResponse:
    return analyze_lead(payload)
