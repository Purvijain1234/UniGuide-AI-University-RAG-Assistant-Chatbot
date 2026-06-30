import streamlit as st
import ollama
from config import *

def build_vector_db(chunks):

    vector_db = []
    progress = st.progress(0)
    status = st.empty()
    total = len(chunks)

    for i, chunk in enumerate(chunks):
        status.text(
            f"Embedding chunk {i+1}/{total}"
        )
        embedding = ollama.embed(
            model=EMBEDDING_MODEL,
            input=chunk["text"]
        )["embeddings"][0]

        vector_db.append(
            {
                "page": chunk["page"],
                "text": chunk["text"],
                "embedding": embedding
            }
        )

        progress.progress(
            (i + 1) / total
        )

    progress.empty()
    status.success("Knowledge Base Ready!")
    return vector_db