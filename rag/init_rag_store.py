from rag_helper import load_docs_and_store_to_chroma

if __name__ == "__main__":
    load_docs_and_store_to_chroma("rag_data")
    print("✅ ChromaDB vector store initialized with RAG data.")
