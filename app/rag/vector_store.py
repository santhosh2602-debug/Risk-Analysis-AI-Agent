import os
import time
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.config import settings

INDEX_PATH = "faiss_risk_index"

def build_vector_store_from_excel(file_path: str) -> FAISS:
    # Initialize Google Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=settings.google_api_key,
        task_type="RETRIEVAL_DOCUMENT"
    )

    if os.path.exists(INDEX_PATH):
        print("--- [RAG] Local Gemini index found. Loading database instantly... ---")
        return FAISS.load_local(
            INDEX_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )

    print(f"--- [RAG] Index not found. Creating Gemini embeddings from {file_path}... ---")
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip() 
    
    documents = []
    for _, row in df.iterrows():
        content = (
            f"Project Type: {row.get('Project Type', 'N/A')} | "
            f"Risk Category: {row.get('Risk Category', 'N/A')} | "
            f"Observation: {row.get('Observation', 'N/A')} | "
            f"Mitigation Plan: {row.get('Mitigation Plan', 'N/A')} | "
            f"Severity: {row.get('Severity', 'N/A')}"
        )
        documents.append(Document(page_content=content))

    batch_size = 5 
    vector_store = FAISS.from_documents(documents[:batch_size], embeddings)

    for i in range(batch_size, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        vector_store.add_documents(batch)
        print(f"Progress: {min(i + batch_size, len(documents))}/{len(documents)} rows embedded...")
        time.sleep(10)

    vector_store.save_local(INDEX_PATH)
    print(f"--- [RAG] Database saved locally to {INDEX_PATH} ---")
    
    return vector_store