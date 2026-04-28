from pydantic import BaseModel, EmailStr, Field, field_validator


class LeadRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Lead's full name")
    email: EmailStr = Field(..., description="Lead's email address")
    company_name: str = Field(..., min_length=2, max_length=120, description="Company name")
    industry: str = Field(..., min_length=2, max_length=80, description="Industry type")
    budget_usd: float = Field(..., ge=0, le=1_000_000_000, description="Available budget in USD")
    message: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Lead's inquiry message",
    )
    urgency: str = Field(..., description="Urgency level provided by the lead")

    @field_validator("full_name", "company_name", "industry", "message", "urgency")
    @classmethod
    def strip_and_require_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned

    @field_validator("urgency")
    @classmethod
    def validate_urgency(cls, value: str) -> str:
        allowed = {"low", "medium", "high"}
        normalized = value.strip().lower()
        if normalized not in allowed:
            raise ValueError("Urgency must be one of: low, medium, high.")
        return normalized


class LeadAnalysisResponse(BaseModel):
    lead_score: int = Field(..., ge=0, le=100, description="Lead score from 0 to 100")
    priority: str = Field(..., description="Priority tier: low, medium, or high")
    summary: str = Field(..., min_length=5, max_length=500)
    recommended_action: str = Field(..., min_length=5, max_length=300)
    reasoning: str = Field(..., min_length=5, max_length=1000)

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        allowed = {"low", "medium", "high"}
        normalized = value.strip().lower()
        if normalized not in allowed:
            raise ValueError("Priority must be one of: low, medium, high.")
        return normalized
