# 🎓 University RAG Assistant

**UniGuide Ai** - An AI-powered **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload a university brochure (PDF) and ask questions about admissions, fees, placements, scholarships, eligibility, hostel facilities, and more.

Instead of manually searching through hundreds of pages, the chatbot retrieves the most relevant sections of the brochure and generates accurate responses using a Large Language Model (LLM).

---

## 🚀 Features

- 📄 Upload any University Brochure (PDF)
- 🤖 AI-powered Question Answering
- 🔍 Semantic Search using Embeddings
- 📚 Retrieval-Augmented Generation (RAG)
- 📖 Source Page References
- 💬 Interactive Chat Interface
- ⚡ Real-time Streaming Responses
- 🧠 Local LLM using Ollama
- 🎨 Modern Streamlit UI

---

# 🏗 Project Structure

```
University-RAG-Assistant/
│
├── app.py
├── config.py
├── requirements.txt
│
├── utils/
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── prompts.py
│
└──  README.md
```

---

# ⚙️ Tech Stack

| Category | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Language | Python |
| PDF Processing | PyMuPDF |
| Embeddings | BGE Base Embedding Model |
| LLM | Llama 3.2 (Ollama) |
| Retrieval | Cosine Similarity |
| AI Framework | Ollama |

---

# 🧠 How It Works

```
                 Upload PDF
                      │
                      ▼
             Extract PDF Text
                      │
                      ▼
              Split into Chunks
                      │
                      ▼
           Generate Embeddings
                      │
                      ▼
             Create Vector Database
                      │
──────────────────────────────────────────────
               User asks Question
                      │
                      ▼
          Generate Query Embedding
                      │
                      ▼
          Semantic Similarity Search
                      │
                      ▼
           Retrieve Relevant Chunks
                      │
                      ▼
             Build Context Prompt
                      │
                      ▼
               Llama (Ollama)
                      │
                      ▼
               Generate Answer
                      │
                      ▼
          Display Sources + Response
```

---

# 📂 Modules

## app.py

Main Streamlit application.

Responsible for:

- User Interface
- PDF Upload
- Chat Interface
- Streaming Responses

---

## pdf_loader.py

Reads PDF using PyMuPDF.

- Extracts text
- Stores page numbers

---

## chunking.py

Splits extracted text into overlapping chunks.

Purpose:

- Better semantic search
- Improved retrieval accuracy

---

## embeddings.py

Generates embeddings for every text chunk using Ollama.

---

## retrieval.py

Implements Retrieval-Augmented Generation.

Functions:

- Cosine Similarity
- Semantic Search
- Top-K Retrieval
- Context Building

---

## prompts.py

Contains the system prompt used by the LLM.

Ensures:

- No hallucinations
- Answers only from brochure
- Page-aware responses

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/University-RAG-Assistant.git
```

Move into the project

```bash
cd University-RAG-Assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Install Ollama

Download Ollama

https://ollama.com

Pull the required models

```bash
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf

ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

---

# ▶️ Run the Project

```bash
streamlit run app.py
```

---

# 💡 Example Questions

You can ask questions like:

- What is the admission process?
- What is the hostel fee?
- What is the placement percentage?
- Which companies visit the campus?
- What scholarships are available?
- What is the eligibility for B.Tech?
- What is the application deadline?
- What is the fee structure?

---

# 📈 Future Improvements

- FAISS Vector Database
- ChromaDB Support
- Multi-PDF Chat
- Compare Universities
- AI-generated Brochure Summary
- Voice Assistant
- Multi-language Support
- PDF Highlighting
- Chat Export
- Citation Links

---

# 📚 RAG Workflow

```
PDF
 │
 ▼
Extract Text
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Vector Database
 │
 ▼
User Query
 │
 ▼
Embedding
 │
 ▼
Similarity Search
 │
 ▼
Relevant Chunks
 │
 ▼
LLM
 │
 ▼
Answer
```

---

# 🤝 Contributing

Contributions are welcome.

Feel free to fork the repository and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

**Purvi Jain**

AI/ML Enthusiast | B.Tech Artificial Intelligence

GitHub: https://github.com/Purvijain1234

LinkedIn: https://www.linkedin.com/in/purvi-jain-315683326/
