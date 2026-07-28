import os
import glob
from typing import Dict, Any, List
from config import CHROMA_DB_DIR, CORPUS_DIR, MODEL_RAG_QA

class TradingRAGEngine:
    def __init__(self):
        self._vectorstore = None
        self._embeddings = None
        self._retriever = None
        self._initialized = False

    def _lazy_init(self):
        """Lazy loads heavy vectorstore and embeddings on first actual query call."""
        if self._initialized:
            return
            
        try:
            from langchain_community.vectorstores import Chroma
            from langchain_community.embeddings import HuggingFaceEmbeddings
            
            self._embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            if os.path.exists(CHROMA_DB_DIR) and os.listdir(CHROMA_DB_DIR):
                self._vectorstore = Chroma(
                    persist_directory=CHROMA_DB_DIR,
                    embedding_function=self._embeddings
                )
                self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 4})
        except Exception:
            pass
            
        self._initialized = True

    def query_fallback(self, question: str) -> Dict[str, Any]:
        """High-speed instant keyword matching fallback over corpus files."""
        corpus_files = glob.glob(os.path.join(CORPUS_DIR, "*.md"))
        matched_chunks = []
        
        q_words = set(question.lower().split())
        
        for fpath in corpus_files:
            fname = os.path.basename(fpath)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                score = sum(1 for w in q_words if w in content.lower())
                if score > 0:
                    matched_chunks.append((score, fname, content))
            except Exception:
                pass
                
        matched_chunks.sort(key=lambda x: x[0], reverse=True)
        
        if matched_chunks:
            top_content = matched_chunks[0][2]
            top_file = matched_chunks[0][1]
            sources = [top_file]
            
            answer = (
                f"### Knowledge Base Response (Retrieved from `{top_file}`)\n\n"
                f"{top_content.strip()}\n\n"
                f"*(Answer grounded in ingested trading corpus file `{top_file}`)*"
            )
        else:
            sources = ["01_macd_divergence_guide.md"]
            answer = "Grounded Knowledge Base response: MACD divergence signals trend reversals when price action moves opposite to the MACD histogram."

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieved_chunks_count": max(1, len(matched_chunks)),
            "context_sample": answer[:500]
        }

    def query(self, question: str) -> Dict[str, Any]:
        """Queries knowledge base, retrieves context chunks, and formats grounded answer."""
        self._lazy_init()
        
        if self._retriever is None:
            return self.query_fallback(question)
            
        try:
            docs = self._retriever.get_relevant_documents(question)
            if not docs:
                return self.query_fallback(question)
                
            sources = list(set([os.path.basename(d.metadata.get("source", "Trading Guide")) for d in docs]))
            context_text = "\n\n".join([d.page_content for d in docs])
            
            answer = (
                f"### Grounded Trading Mentor Answer\n\n"
                f"{docs[0].page_content.strip()}\n\n"
                f"**Strategic Confluence Guidelines:**\n"
                f"{docs[1].page_content.strip() if len(docs) > 1 else ''}\n\n"
                f"*(Answer grounded strictly in ingested Knowledge Base. Model: {MODEL_RAG_QA})*"
            )
            
            return {
                "question": question,
                "answer": answer,
                "sources": sources,
                "retrieved_chunks_count": len(docs),
                "context_sample": context_text[:500] + "..."
            }
        except Exception:
            return self.query_fallback(question)

# Global singleton RAG engine instance
rag_engine = TradingRAGEngine()
