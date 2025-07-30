import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_aws.embeddings import BedrockEmbeddings

def load_docs_and_store_to_chroma(directory: str, persist_directory: str = "rag/chroma_store"):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(directory, filename))
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)

    embedding = BedrockEmbeddings(
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        model_id="amazon.titan-embed-text-v2:0"  # ✅ New Titan V2 model
    )

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print(f"✅ Stored {len(splits)} chunks to Chroma at {persist_directory}")

def query_chroma(service_name, persist_directory="rag/chroma_store", k=4):
    embedding = BedrockEmbeddings(
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        model_id="amazon.titan-embed-text-v2:0"
    )
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    return vectordb.similarity_search(service_name, k=k)
