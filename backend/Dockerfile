FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV OLLAMA_HOST=http://ollama:11434
ENV EMBED_MODEL=bge-small-en-v1.5
ENV CHROMA_DIR=/app/vectorstore

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
