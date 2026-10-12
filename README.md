# Finance Agent – Google ADK demo

A small AI agent built with Google Agent Development Kit (ADK) and Gemini.
It answers expense questions for an admin/finance office.

## Features
- Two Python tools: total spend by category, budget overrun check
- The model never calculates numbers itself: it always calls the tools
- Audit log of every tool call (traceability)
- Fake data only, no personal data (privacy by design)

## Run it
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example finance_agent/.env   # then add your Gemini API key
adk web
```
Open http://127.0.0.1:8000 and select `finance_agent`.

## Next steps
- Read expenses from Google Sheets
- Deploy on Vertex AI
- Retry and fallback model on 503 errors