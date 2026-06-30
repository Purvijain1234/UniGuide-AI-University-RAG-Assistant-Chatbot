import streamlit as st
import ollama
from config import *

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.
    """

    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (norm1 * norm2)


def retrieve(query, top_k=5):
    """
    Retrieve the most relevant chunks.
    """

    query_embedding = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query
    )["embeddings"][0]

    scored_chunks = []

    for item in st.session_state.vector_db:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        scored_chunks.append(
            {
                "page": item["page"],
                "text": item["text"],
                "score": similarity
            }
        )

    scored_chunks.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    filtered = [
    item
    for item in scored_chunks
    if item["score"] > 0.45
]

    return filtered[:top_k]
    

def build_context(retrieved_chunks):
    """
    Convert retrieved chunks into a prompt context.
    """

    context = ""

    for chunk in retrieved_chunks:

        context += (
            f"\n\n========== PAGE {chunk['page']} ==========\n"
        )

        context += chunk["text"]

    return context