# Banking Customer Support AI Agent (Starter)

This starter implements the capstone's three agent paths, unique six-digit ticket creation, SQLite support tickets, interaction logs, and a Streamlit dashboard.

**Important:** Phase 1 uses transparent rules, *not an LLM*. It is a baseline prototype. Phase 2 should add an actual LLM for classification and personalized responses and measure accuracy, routing success, empathy, and clarity.

## Run on Windows PowerShell

```powershell
cd banking_ai_agent_starter
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m streamlit run app.py` directly.

Open `http://localhost:8501` if your browser doesn't open automatically.

## Demo

1. Submit `Thanks for resolving my net banking issue.` -> Positive Feedback
2. Submit `My debit card replacement has not arrived.` -> Negative Feedback; ticket created
3. Copy the displayed ticket number, submit `What is the status of ticket XXXXXX?` -> ticket status
4. Open Tickets and Agent Logs tabs

## Tests

```powershell
python -m pytest -q
```

## Data / safety

SQLite data is written to `banking_support.db` in the project directory. Use only fictional customer names and test messages. This is a learning demonstration, not a production banking tool. The demo has no authentication, so it should not be exposed publicly with sensitive records.
