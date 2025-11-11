# AI Course Builder (OSS, local-first)

**Free and local-first** course builder that:
- Ingests PDFs/URLs/text
- Generates a structured **course outline** (modules, outcomes, readings, milestones)
- Produces **MCQs** per module with correct answers and explanations

Stack: **FastAPI** · **ChromaDB** · **Sentence-Transformers** · **Ollama (Llama 3.1 8B by default)**  
No paid APIs required. Runs fully offline after models are pulled once.

---

## ✨ Features
- `/ingest` — load PDF/URL/raw text and chunk to vector store
- `/outline` — curriculum designer (weeks, goals-aware)
- `/quiz` — N MCQs with explanations, grounded by retrieved context (RAG)

## 🧱 Architecture
- **API:** FastAPI
- **Vector store:** ChromaDB (persistent)
- **Embeddings:** `bge-small-en-v1.5` (default) or any ST model
- **Retrieval:** dense + BM25 re-rank
- **LLM:** Ollama (`llama3.1:8b` by default; configurable via env)

```
ai-course-builder/
├─ backend/
│  ├─ app/
│  │  ├─ main.py          # FastAPI endpoints
│  │  ├─ rag.py           # ChromaDB + hybrid retrieve
│  │  ├─ quiz.py          # quiz prompt
│  │  └─ utils.py         # pdf/url readers + chunker
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ README.md
├─ data/                  # put your PDFs here
├─ vectorstore/           # persisted Chroma DB
├─ docker-compose.yml
├─ .github/workflows/ci.yml
├─ .gitignore
├─ LICENSE
├─ CONTRIBUTING.md
└─ Makefile
```

---

## 🚀 Quickstart

> Requires **Docker Desktop**.

```bash
git clone https://github.com/<you>/ai-course-builder.git
cd ai-course-builder
docker compose up -d

# pull a model inside the ollama container
docker exec -it ollama ollama pull llama3.1:8b

# open docs
open http://localhost:8000/docs   # (Windows: start http://localhost:8000/docs)
```

### Try it
1. Use `/ingest` to upload a PDF or a URL.  
2. Call `/outline` with `{ "topic": "Graph Neural Networks", "weeks": 4, "goals": "projects + math-lite" }`.  
3. Call `/quiz` with the outline (paste outline string or JSON) and number of questions.

---

## ⚙️ Configuration
Env vars (configured in `docker-compose.yml`):
- `OLLAMA_HOST` — default `http://ollama:11434`
- `MODEL` — default `llama3.1:8b` (try `mistral:7b` for lower RAM)
- `EMBED_MODEL` — default `bge-small-en-v1.5`
- `CHROMA_DIR` — default `/app/vectorstore`

---

## 🧪 Testing (minimal smoke test)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
# then run tests
pytest -q
```

---

## 🛣️ Roadmap ideas
- Next.js UI with auth (Clerk/Auth.js), sessioned courses and progress
- Better evals (faithfulness, hallucination filters, question quality)
- Export courses to Markdown/PDF; quiz CSV
- Multi-doc ingestion pipelines & async jobs
- Rerankers (colbert-lite), retrieval fusion

---

## 🧾 License
MIT — do whatever, no warranty (see LICENSE).

---

## 🙌 Contributing
See `CONTRIBUTING.md`. PRs welcome!
