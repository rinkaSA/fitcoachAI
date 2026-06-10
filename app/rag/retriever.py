import json
from typing import List, Dict

import numpy as np
from google import genai

from app.config import GEMINI_API_KEY, VECTOR_STORE_PATH, EMBEDDING_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def load_vector_store() -> List[Dict]:
    if not VECTOR_STORE_PATH.exists():
        raise FileNotFoundError(
            f"Vector store not found at {VECTOR_STORE_PATH}. "
            "Run: uv python -m app.rag.build_vector_store"
        )

    return json.loads(VECTOR_STORE_PATH.read_text(encoding="utf-8"))


def create_query_embedding(query: str) -> List[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
    )

    return response.embeddings[0].values


def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
    a = np.array(vector_a, dtype=np.float32)
    b = np.array(vector_b, dtype=np.float32)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def retrieve_relevant_chunks(query: str, top_k: int = 4) -> List[Dict]:
    vector_store = load_vector_store()
    query_embedding = create_query_embedding(query)

    scored_chunks = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])

        scored_chunks.append(
            {
                "id": item["id"],
                "source": item["source"],
                "chunk_index": item["chunk_index"],
                "content": item["content"],
                "score": score,
            }
        )

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    return scored_chunks[:top_k]

# to do!! safety hybrid retrival : embedding search with keywords/ rule triggers like
# SAFETY_TERMS = ["pain", "sharp pain", "injury", "dizzy", "numb", "swollen"]

#if any(term in query.lower() for term in SAFETY_TERMS):
#always_include("01_recovery_rules.md")