from langchain_community.vectorstores import FAISS

class ContextRetriever:
    def __init__(self, vector_store: FAISS):
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int) -> str:
        docs = self.vector_store.similarity_search(query, k=k)
        
        return "\n---\n".join(d.page_content for d in docs)