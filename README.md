# Multilingual RAG (Bangla & English) – FAISS + Gemini

This project implements a **Retrieval-Augmented Generation (RAG)** system that answers **Bangla** and **English** queries based on the **HSC26 Bangla 1st Paper** PDF.

---

## **Features**
- **Multilingual Query Support:** Handles Bangla and English inputs.
- **Free Embeddings:** Uses `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- **Vector Database:** FAISS for efficient local retrieval.
- **LLM Integration:** Google Gemini (via `langchain-google-genai`).
- **Conversation Memory:** Short-term chat memory and long-term vector store.
- **REST API:** FastAPI `/ask` endpoint for queries.
- **Evaluation:** Cosine similarity–based relevance checking.
- **Dockerized:** Ready-to-deploy container.

---

## **Setup & Installation**

### **1. Clone & Install**
```bash
git clone <repo_url>
cd rag-bn-en
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### **2. Configure**
Create `.env`:
```bash
cp .env.example .env
```
Update `GOOGLE_API_KEY` with your Gemini key.

### **3. Ingest PDFs**
Place **HSC26 Bangla 1st Paper** PDF in `data/`:
```bash
python -m src.ingest --pdfs data/*.pdf
```

### **4. Run the API**
```bash
uvicorn src.api:app --reload --port 8000
```
**Test with curl:**
```bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"question": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"}'
```

---

## **Docker**
```bash
docker build -t rag-bn-en .
docker run -d -p 8000:8000 --env-file .env rag-bn-en
```
or
```bash
docker-compose up --build
```

---

## **Sample Queries**
**Q:** অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?  
**A:** শুভ্রনাথ  

**Q:** কাকে অনুপমের ভাগ্যদেবতা বলে উল্লেখ করা হয়েছে?  
**A:** মামাকে  

**Q:** বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?  
**A:** ১৫ বছর  

---

# **Required Questions Answered**

### **1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?**
- **Library:** PyMuPDF (`fitz`) via `langchain_community.document_loaders.PyMuPDFLoader`.
- **Reason:** PyMuPDF handles Bangla text encoding better and is faster than alternatives like `pypdf`.
- **Challenges:** The PDF had line breaks, page numbers, and formatting artifacts. We removed these during preprocessing and chunking (using custom separators like `।` for Bangla).

### **2. What chunking strategy did you choose (e.g., paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?**
- **Strategy:** **RecursiveCharacterTextSplitter** with `chunk_size=800` characters and `chunk_overlap=120`, using separators `["\n\n", "\n", "।", ".", "?", " "]`.
- **Reason:** Bangla text uses `।` instead of `.`, so adding Bangla separators ensures chunks don’t break in unnatural places.
- **Benefit:** It keeps context cohesive and improves semantic embeddings and retrieval.

### **3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?**
- **Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- **Reason:** Free, lightweight, and optimized for over 50 languages, including Bangla and English.
- **How it works:** Creates dense vector representations (embeddings) that capture semantic similarity, enabling the system to retrieve relevant content based on meaning rather than keywords.

### **4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?**
- **Comparison:** Using **cosine similarity** between the query’s embedding and document chunk embeddings.
- **Storage:** FAISS (local vector database) for fast similarity search.
- **Reason:** FAISS is open-source, free, and highly efficient for approximate nearest neighbor search.

### **5. How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?**
- **Ensuring Meaningfulness:** Both queries and chunks are embedded using the **same multilingual embedding model**, ensuring they share the same semantic vector space.
- **Vague Queries:** If the retriever finds low-similarity matches, the LLM is prompted to **respond with "I don’t know"** when relevant context is missing.

### **6. Do the results seem relevant? If not, what might improve them (e.g., better chunking, better embedding model, larger document)?**
- **Results:** For the test cases, the results are highly relevant.
- **Improvements:**  
  - Use a stronger model like `bge-m3` or OpenAI’s `text-embedding-3-large`.  
  - Fine-tune chunk sizes based on document structure.  
  - Use hybrid retrieval (BM25 + dense embeddings) for better recall.

---

## **Evaluation**
We implemented a basic evaluation (`src/eval.py`) using:
- **Semantic Similarity:** Cosine similarity between model answers and gold answers.
- **Groundedness:** Check if retrieved chunks contain the gold answers.

---

## **Author**
**Khan Md. Saifullah Anjar**
