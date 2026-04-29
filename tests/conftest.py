import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


VALID_LEAD_PAYLOAD = {
    "full_name": "Jordan Lee",
    "email": "jordan.lee@acmecorp.com",
    "company_name": "Acme Corp",
    "industry": "SaaS",
    "budget_usd": 25000,
    "message": "We need automation support for lead qualification and CRM integration.",
    "urgency": "high",
}

EXPECTED_RESPONSE_FIELDS = frozenset(
    {"lead_score", "priority", "summary", "recommended_action", "reasoning"}
)


def _mock_openai_completion_json(data: dict) -> MagicMock:
    completion = MagicMock()
    completion.choices = [MagicMock()]
    completion.choices[0].message.content = json.dumps(data)
    return completion


@pytest.fixture
def mock_openai_success():
    """Patches OpenAI in lead_service so no real API calls occur."""
    payload = {
        "lead_score": 82,
        "priority": "high",
        "summary": "Strong SaaS lead with budget and clear automation intent.",
        "recommended_action": "Schedule a discovery call within 24 hours.",
        "reasoning": "High budget, high urgency, and message references CRM automation.",
    }
    completion = _mock_openai_completion_json(payload)
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = completion

    with patch("app.services.lead_service.OpenAI", return_value=mock_client) as mock_cls:
        yield mock_cls


@pytest.fixture
def app_client(mock_openai_success, monkeypatch):
    """TestClient with fake OpenAI API key and mocked OpenAI client."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used-real-api")
    from app.main import app

    with TestClient(app) as c:
        yield c
