import json
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

from app.schemas.lead_schema import LeadAnalysisResponse, LeadRequest

load_dotenv()


def _build_prompt(lead: LeadRequest) -> str:
    return (
        "You are an expert sales lead qualification assistant for an automation services agency.\n"
        "Analyze the lead and return only JSON.\n\n"
        "Evaluate these factors:\n"
        "1) Budget size\n"
        "2) Urgency\n"
        "3) Business type / industry\n"
        "4) Message intent\n"
        "5) Likelihood the lead is ready for automation services\n"
        "6) Whether the lead should be followed up quickly\n\n"
        "Required output fields (exact names):\n"
        "- lead_score: integer from 0 to 100\n"
        "- priority: one of low, medium, high\n"
        "- summary: short professional summary\n"
        "- recommended_action: clear next step\n"
        "- reasoning: brief explanation of the scoring logic\n\n"
        f"Lead data:\n"
        f"- full_name: {lead.full_name}\n"
        f"- email: {lead.email}\n"
        f"- company_name: {lead.company_name}\n"
        f"- industry: {lead.industry}\n"
        f"- budget_usd: {lead.budget_usd}\n"
        f"- message: {lead.message}\n"
        f"- urgency: {lead.urgency}\n"
    )


def _extract_text_response(completion) -> str:
    content = completion.choices[0].message.content
    if content is None:
        raise ValueError("Model returned an empty response.")
    return content.strip()


def analyze_lead(lead: LeadRequest) -> LeadAnalysisResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file.",
        )

    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "Return valid JSON only. Do not include markdown or extra text.",
                },
                {"role": "user", "content": _build_prompt(lead)},
            ],
        )

        parsed = json.loads(_extract_text_response(completion))
        return LeadAnalysisResponse.model_validate(parsed)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to analyze lead with OpenAI. Please try again shortly.",
        ) from exc
