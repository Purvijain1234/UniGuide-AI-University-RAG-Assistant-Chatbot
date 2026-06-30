import streamlit as st
import ollama

from config import *
from utils.pdf_loader import load_pdf
from utils.chunking import create_chunks
from utils.embeddings import build_vector_db
from utils.retrieval import retrieve, build_context
from utils.prompts import create_prompt


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="University RAG Assistant",
    page_icon="🎓",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp{
    background:#0E1117;
}

.main-title{
    text-align:center;
    font-size:3rem;
    font-weight:bold;
    background:linear-gradient(90deg,#00DBDE,#FC00FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{
    text-align:center;
    color:#bdbdbd;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "filename" not in st.session_state:
    st.session_state.filename = ""


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🎓 University Brochure")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    st.markdown("---")

    st.subheader("Models")

    st.info(
        f"""
Embedding

{EMBEDDING_MODEL}

LLM

{LANGUAGE_MODEL}
"""
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">🎓 University RAG Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Chat with any University Brochure using RAG + Ollama</div>',
    unsafe_allow_html=True
)


# ==========================================================
# PROCESS PDF
# ==========================================================

if uploaded_file is not None and st.session_state.vector_db is None:

    with st.spinner("Reading PDF..."):
        pages = load_pdf(uploaded_file)

    with st.spinner("Creating Chunks..."):
        chunks = create_chunks(pages)

    with st.spinner("Generating Embeddings..."):
        st.session_state.vector_db = build_vector_db(chunks)

    st.session_state.filename = uploaded_file.name

    st.success(
        f"Loaded {len(chunks)} chunks from {uploaded_file.name}"
    )

if st.session_state.vector_db is not None:

    st.sidebar.success("Knowledge Base Loaded")

    st.sidebar.metric(
        "Chunks",
        len(st.session_state.vector_db)
    )


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def show_retrieved_chunks(retrieved_chunks):

    with st.expander("📚 Retrieved Context", expanded=False):

        for i, chunk in enumerate(retrieved_chunks):

            st.markdown(f"### Result {i + 1}")

            st.write(f"**Page:** {chunk['page']}")

            st.write(
                f"**Similarity:** {chunk['score']:.4f}"
            )

            st.info(
                chunk["text"][:700] + "..."
            )

            st.divider()


# ==========================================================
# DISPLAY CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================================
# CHAT
# ==========================================================

if st.session_state.vector_db is not None:

    query = st.chat_input(
        "Ask anything about the university..."
    )

    if query:

        # -------------------------------
        # USER MESSAGE
        # -------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.markdown(query)

        # -------------------------------
        # RETRIEVE CONTEXT
        # -------------------------------

        retrieved_chunks = retrieve(
            query,
            top_k=5
        )

        show_retrieved_chunks(retrieved_chunks)

        context = build_context(retrieved_chunks)

        system_prompt = create_prompt(context)

        # -------------------------------
        # GENERATE RESPONSE
        # -------------------------------

        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            full_response = ""

            stream = ollama.chat(
                model=LANGUAGE_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                stream=True
            )

            for chunk in stream:

                token = chunk["message"]["content"]

                full_response += token

                response_placeholder.markdown(
                    full_response + "▌"
                )

            # -------------------------------
            # SOURCES
            # -------------------------------

            full_response += "\n\n---\n"
            full_response += "### 📚 Sources\n\n"

            used_pages = []

            for chunk in retrieved_chunks:

                if chunk["page"] not in used_pages:
                    used_pages.append(chunk["page"])

            for page in used_pages:
                full_response += f"📄 Page {page}\n"

            full_response += "\n"
            full_response += "### Retrieved Excerpts\n\n"

            for i, chunk in enumerate(retrieved_chunks):

                preview = (
                    chunk["text"][:250]
                    .replace("\n", " ")
                    .strip()
                )

                full_response += (
                    f"**{i + 1}. Page {chunk['page']}**\n\n"
                )

                full_response += preview + "...\n\n"

            response_placeholder.markdown(full_response)

        # -------------------------------
        # SAVE CHAT
        # -------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

else:

    st.info(
        "👈 Upload a University Brochure PDF to start chatting."
    )