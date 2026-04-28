# AI Lead Form Analyzer (FastAPI)

A portfolio-ready Python backend API that receives website lead form submissions and returns an AI-style lead analysis.

This version uses **placeholder scoring logic** (no real LLM call yet), so you can focus on project structure and API fundamentals first.

## Project Structure

```text
.
├── app/
│   ├── main.py
│   ├── schemas/
│   │   └── lead_schema.py
│   └── services/
│       └── lead_service.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Tech Stack

- FastAPI
- Pydantic
- Uvicorn

## API Endpoint

- `POST /analyze-lead`

### Request Body

```json
{
  "full_name": "Jordan Lee",
  "email": "jordan.lee@acmecorp.com",
  "company_name": "Acme Corp",
  "industry": "SaaS",
  "budget_usd": 25000,
  "message": "We need automation support for lead qualification and CRM integration in the next quarter.",
  "urgency": "high"
}
```

### Response Body (Example)

```json
{
  "lead_score": 85,
  "priority": "high",
  "summary": "Jordan Lee from Acme Corp submitted a high-priority lead in the SaaS industry.",
  "recommended_action": "Schedule a discovery call within 24 hours and prepare a tailored proposal.",
  "reasoning": "This placeholder score combines budget, urgency, message detail, and industry fit. Replace this logic with an LLM-powered analysis in a future step."
}
```

### Screenshot

The screenshot below shows a successful POST /analyze-lead test in FastAPI Swagger UI.

![Swagger UI successful lead analysis response](docs/images/swagger-lead-analysis-code-200.png)

## Getting Started (Beginner-Friendly)

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Create your environment file

```bash
copy .env.example .env
```

On macOS/Linux use:

```bash
cp .env.example .env
```

### 4) Run the API

```bash
uvicorn app.main:app --reload
```

API base URL:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 5) Open automatic API docs

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Notes for Next Iteration

- Replace placeholder logic in `app/services/lead_service.py` with an OpenAI (or other LLM) call.
- Add unit tests for schema validation and scoring behavior.
- Add persistent storage for analyzed leads.
