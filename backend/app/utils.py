\
import os, re, requests
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
from readability import Document

def read_pdf(path: str) -> str:
    """Extract plain text from a PDF."""
    return extract_text(path)

def read_url(url: str) -> str:
    """Fetch URL and extract readable text with basic cleanup."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    html = resp.text
    doc = Document(html)
    text_html = doc.summary()
    soup = BeautifulSoup(text_html, "html.parser")
    text = soup.get_text("\n")
    return re.sub(r"\n{2,}", "\n\n", text).strip()

def chunk(text: str, max_tokens: int = 700, overlap: int = 120):
    """Naive token-ish chunking by words with overlap."""
    words = text.split()
    step = max_tokens - overlap
    if step <= 0:
        step = max_tokens
    for i in range(0, len(words), step):
        yield " ".join(words[i:i+max_tokens])
