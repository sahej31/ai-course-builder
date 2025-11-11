import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

EMBED_NAME = os.getenv("EMBED_MODEL", "bge-small-en-v1.5")

class RAGStore:
    def __init__(self, persist_dir: str):
        self.client = chromadb.Client(Settings(persist_directory=persist_dir, anonymized_telemetry=False))
        try:
            self.col = self.client.get_collection("courses")
        except Exception:
            self.col = self.client.create_collection("courses")
        self.embedder = SentenceTransformer(EMBED_NAME)

    def reset(self):
        try:
            self.client.delete_collection("courses")
        except Exception:
            pass
        self.col = self.client.create_collection("courses")

    def add_docs(self, docs, metadatas):
        embs = self.embedder.encode(docs, show_progress_bar=False).tolist()
        ids = [f"d{i}" for i in range(len(docs))]
        self.col.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embs)

    def retrieve(self, query, k=6):
        q_emb = self.embedder.encode([query]).tolist()[0]
        dense = self.col.query(query_embeddings=[q_emb], n_results=max(k, 6))
        dense_docs = dense.get("documents", [[]])[0]
        dense_meta = dense.get("metadatas", [[]])[0]

        if not dense_docs:
            return []

        bm25 = BM25Okapi([d.split() for d in dense_docs])
        order = bm25.get_top_n(query.split(), dense_docs, n=min(k, len(dense_docs)))
        meta_map = {dense_docs[i]: dense_meta[i] for i in range(len(dense_docs))}
        return [(d, meta_map.get(d, {})) for d in order]
