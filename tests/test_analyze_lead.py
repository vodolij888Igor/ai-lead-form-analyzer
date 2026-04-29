from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import EXPECTED_RESPONSE_FIELDS, VALID_LEAD_PAYLOAD


def test_analyze_lead_success_returns_200(app_client: TestClient):
    response = app_client.post("/analyze-lead", json=VALID_LEAD_PAYLOAD)
    assert response.status_code == 200


def test_analyze_lead_response_has_exact_required_fields(app_client: TestClient):
    response = app_client.post("/analyze-lead", json=VALID_LEAD_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == EXPECTED_RESPONSE_FIELDS


def test_analyze_lead_lead_score_is_int_in_range(app_client: TestClient):
    response = app_client.post("/analyze-lead", json=VALID_LEAD_PAYLOAD)
    assert response.status_code == 200
    score = response.json()["lead_score"]
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_analyze_lead_priority_is_valid_enum(app_client: TestClient):
    response = app_client.post("/analyze-lead", json=VALID_LEAD_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["priority"] in ("low", "medium", "high")


@pytest.mark.parametrize(
    "payload_overrides",
    [
        {"full_name": ""},
        {"email": "not-an-email"},
        {"urgency": "critical"},
        {"budget_usd": -1},
    ],
)
def test_analyze_lead_invalid_body_returns_422(payload_overrides: dict):
    """Validation runs before the handler; no OpenAI call or API key required."""
    from app.main import app

    bad = {**VALID_LEAD_PAYLOAD, **payload_overrides}
    with TestClient(app) as client:
        response = client.post("/analyze-lead", json=bad)
    assert response.status_code == 422


def test_analyze_lead_missing_required_field_returns_422():
    from app.main import app

    incomplete = {k: v for k, v in VALID_LEAD_PAYLOAD.items() if k != "message"}
    with TestClient(app) as client:
        response = client.post("/analyze-lead", json=incomplete)
    assert response.status_code == 422


def test_analyze_lead_missing_openai_api_key_returns_503(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def getenv_no_openai_key(key: str, default=None):
        if key == "OPENAI_API_KEY":
            return None
        import os

        return os.environ.get(key, default)

    with patch("app.services.lead_service.os.getenv", side_effect=getenv_no_openai_key):
        with patch("app.services.lead_service.OpenAI") as mock_openai_cls:
            from app.main import app

            with TestClient(app) as client:
                response = client.post("/analyze-lead", json=VALID_LEAD_PAYLOAD)

    assert response.status_code == 503
    assert "OpenAI API key" in response.json().get("detail", "")
    mock_openai_cls.assert_not_called()


def test_analyze_lead_openai_failure_returns_502(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used-real-api")
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = RuntimeError("Simulated OpenAI outage")

    with patch("app.services.lead_service.OpenAI", return_value=mock_client):
        from app.main import app

        with TestClient(app) as client:
            response = client.post("/analyze-lead", json=VALID_LEAD_PAYLOAD)

    assert response.status_code == 502
    detail = response.json().get("detail", "")
    assert "OpenAI" in detail or "try again" in detail.lower()
