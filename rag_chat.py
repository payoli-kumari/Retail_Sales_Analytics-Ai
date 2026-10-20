"""AI Feature 2: RAG - answer questions from the project documents (docs/*.md)."""
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from llm import chat

DOCS = Path(__file__).parent / "docs"

# The exact sentence the AI must use when the answer is not in the documents
NOT_FOUND = "Not found in the project documents."

# 1) Split documents into chunks (one paragraph = one chunk).
# The regex splits on blank lines and works with both Windows (\r\n) and Linux (\n) files.
chunks = []
for f in sorted(DOCS.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    for para in re.split(r"\n\s*\n", text):
        if len(para.strip()) > 40:
            chunks.append(f"[{f.name}] {para.strip()}")

if not chunks:
    raise RuntimeError("No text found in the docs/ folder. "
                       "Fill data_dictionary.md and project_notes.md, then save them.")

# 2) Build the search index (TF-IDF = word matching).
# stop_words="english" ignores common words like "what", "was", "in",
# so the match depends on the meaningful keywords only.
vec = TfidfVectorizer(stop_words="english")
matrix = vec.fit_transform(chunks)


def retrieve(question: str, k: int = 3):
    """3) Find the k chunks most similar to the question."""
    sims = cosine_similarity(vec.transform([question]), matrix)[0]
    return [chunks[i] for i in sims.argsort()[::-1][:k]]


def ask_project(question: str):
    """4) Give only those chunks to the AI and ask it to answer from them."""
    context = "\n\n".join(retrieve(question))
    answer = chat(
        "Answer ONLY from the given context. Reply in English only. "
        f"If the answer is not in the context, reply exactly: '{NOT_FOUND}'",
        f"Context:\n{context}\n\nQuestion: {question}")
    return answer, context