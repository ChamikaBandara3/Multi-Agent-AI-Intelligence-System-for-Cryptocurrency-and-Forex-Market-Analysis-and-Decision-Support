import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_DB_DIR, CORPUS_DIR

def ingest_trading_corpus():
    """
    Ingests 21+ domain-specific trading guides into ChromaDB vectorstore.
    Chunking Strategy: RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=150)
    Embedding Model: SentenceTransformers all-MiniLM-L6-v2 (Free, fast, local embedding)
    Vector Store: ChromaDB
    """
    corpus_path = Path(CORPUS_DIR)
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus directory not found at {CORPUS_DIR}")
        
    print(f"Loading documents from {CORPUS_DIR}...")
    loader = DirectoryLoader(str(corpus_path), glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} Markdown files.")
    
    # Document Chunking Strategy
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Generated {len(chunks)} text chunks from domain corpus.")
    
    # Embedding Model Setup
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Vectorstore Build
    print(f"Embedding and building ChromaDB vector database in {CHROMA_DB_DIR}...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    print("Vector database successfully built and persisted!")
    return vectorstore

if __name__ == "__main__":
    ingest_trading_corpus()
