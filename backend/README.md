# Backend

Run locally without Docker:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OLLAMA_HOST=http://localhost:11434
uvicorn app.main:app --reload
```
