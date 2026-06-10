import json
from pathlib import Path
from typing import List, Dict

from google import genai

from app.config import (
    GEMINI_API_KEY,
    KNOWLEDGE_DIR,
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL,
)

client = genai.Client(api_key=GEMINI_API_KEY)


def read_markdown_files() -> List[Dict]:
    documents = []

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents


def chunk_text(text: str, max_chars: int = 800, overlap: int = 120) -> List[str]:
    """
    Super simple character-based chunking. Use it as a fallback if the next chunking-by-headings produce chunks too large.
    to do: make it sentence based? rfind('.') ?
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks

def chunk_markdown_by_headings(text: str, max_chars: int = 1000) -> list[str]:
    "More advanced chunking but still very intuitive"
    sections = []
    current = []

    for line in text.splitlines():
        if line.startswith("#") and current:
            sections.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    final_chunks = []

    for section in sections:
        if len(section) <= max_chars:
            final_chunks.append(section)
        else:
            final_chunks.extend(chunk_text(section, max_chars=max_chars))

    return [chunk for chunk in final_chunks if chunk]


def create_embedding(text: str) -> List[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


def build_vector_store() -> None:
    documents = read_markdown_files()
    vector_store = []

    for document in documents:
        source = document["source"]
        chunks = chunk_markdown_by_headings(document["content"])

        for index, chunk in enumerate(chunks):
            print(f"Embedding {source} chunk {index + 1}/{len(chunks)}")

            embedding = create_embedding(chunk)

            vector_store.append( # to do: add metadate edited at for stale embeddings 
                {
                    "id": f"{source}::chunk_{index}",
                    "source": source,
                    "chunk_index": index,
                    "content": chunk,
                    "embedding": embedding,
                }
            )

    VECTOR_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    VECTOR_STORE_PATH.write_text(
        json.dumps(vector_store, indent=2),
        encoding="utf-8",
    )

    print(f"Save {len(vector_store)} chunks to {VECTOR_STORE_PATH}")


if __name__ == "__main__":
    build_vector_store()