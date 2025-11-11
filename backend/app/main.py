import os, json, requests
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from .utils import read_pdf, read_url, chunk
from .rag import RAGStore
from .quiz import quiz_prompt

OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.1:8b")
store = RAGStore(persist_dir=os.getenv("CHROMA_DIR", "./vectorstore"))

app = FastAPI(title="AI Course Builder (OSS)")

class OutlineReq(BaseModel):
    topic: str
    goals: str = ""
    weeks: int = 4

class QuizReq(BaseModel):
    topic: str
    outline: list | str
    num_questions: int = 6

def ollama_chat(prompt: str, temp=0.2):
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": prompt, "options": {"temperature": temp}},
        timeout=180)
    r.raise_for_status()
    return r.json().get("response", "")

@app.post("/ingest")
async def ingest(source_type: str = Form(...), value: str = Form(None), file: UploadFile | None = None):
    texts, metas = [], []
    if source_type == "pdf" and file:
        data = await file.read()
        path = f"/tmp/{file.filename}"
        with open(path, "wb") as f:
            f.write(data)
        t = read_pdf(path)
        for i, ch in enumerate(chunk(t)):
            texts.append(ch); metas.append({"type":"pdf","name":file.filename,"chunk":i})
    elif source_type == "url" and value:
        t = read_url(value)
        for i, ch in enumerate(chunk(t)):
            texts.append(ch); metas.append({"type":"url","url":value,"chunk":i})
    elif source_type == "text" and value:
        for i, ch in enumerate(chunk(value)):
            texts.append(ch); metas.append({"type":"text","chunk":i})
    else:
        return {"ok": False, "error": "invalid source"}

    if not texts:
        return {"ok": False, "error": "no content"}

    store.add_docs(texts, metas)
    return {"ok": True, "chunks": len(texts)}

@app.post("/outline")
def outline(req: OutlineReq):
    ctx = store.retrieve(req.topic, k=6)
    ctx_text = "\n\n".join([c[0] for c in ctx])
    prompt = f"""
You are a curriculum designer. Create a {req.weeks}-week course for the topic:
"{req.topic}". Include weekly modules with 3-5 bullet learning outcomes,
a reading list (mix textbooks, blogs, videos), and milestone projects.
Constraints: align with goals = "{req.goals}". Keep it concise but actionable.
Use the context if relevant:

Context:
{ctx_text[:4000]}
""".strip()
    resp = ollama_chat(prompt)
    return {"outline": resp}

@app.post("/quiz")
def quiz(req: QuizReq):
    ctx = store.retrieve(req.topic, k=6)
    ctx_text = "\n\n".join([c[0] for c in ctx])
    prompt = quiz_prompt(req.topic, req.outline, ctx_text, req.num_questions)
    resp = ollama_chat(prompt, temp=0.1)
    try:
        qs = json.loads(resp)
    except Exception:
        qs = [{"raw": resp}]
    return {"quiz": qs}
