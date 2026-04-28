from app.schemas.lead_schema import LeadAnalysisResponse, LeadRequest


def _calculate_placeholder_score(lead: LeadRequest) -> int:
    score = 0

    if lead.budget_usd >= 50_000:
        score += 35
    elif lead.budget_usd >= 10_000:
        score += 25
    elif lead.budget_usd > 0:
        score += 15

    if lead.urgency == "high":
        score += 30
    elif lead.urgency == "medium":
        score += 20
    else:
        score += 10

    if len(lead.message) >= 150:
        score += 20
    elif len(lead.message) >= 60:
        score += 15
    else:
        score += 8

    if lead.industry.lower() in {"saas", "fintech", "healthcare", "ecommerce"}:
        score += 15
    else:
        score += 8

    return min(score, 100)


def _derive_priority(lead_score: int) -> str:
    if lead_score >= 75:
        return "high"
    if lead_score >= 45:
        return "medium"
    return "low"


def analyze_lead(lead: LeadRequest) -> LeadAnalysisResponse:
    lead_score = _calculate_placeholder_score(lead)
    priority = _derive_priority(lead_score)

    summary = (
        f"{lead.full_name} from {lead.company_name} submitted a "
        f"{priority}-priority lead in the {lead.industry} industry."
    )
    recommended_action = {
        "high": "Schedule a discovery call within 24 hours and prepare a tailored proposal.",
        "medium": "Send a personalized follow-up email with relevant case studies this week.",
        "low": "Add to nurture campaign and re-engage with educational content.",
    }[priority]

    reasoning = (
        "This placeholder score combines budget, urgency, message detail, and "
        "industry fit. Replace this logic with an LLM-powered analysis in a future step."
    )

    return LeadAnalysisResponse(
        lead_score=lead_score,
        priority=priority,
        summary=summary,
        recommended_action=recommended_action,
        reasoning=reasoning,
    )
