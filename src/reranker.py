from typing import List
from sentence_transformers import CrossEncoder
from langchain_core.documents import Document


class Reranker:
    """
    Local cross-encoder reranker.
    Reorders retrieved documents based on how well they answer the query.
    """

    def __init__(self):
        # Lightweight, fast, fully local model
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        docs: List[Document],
        top_n: int = 5
    ) -> List[Document]:
        if not docs:
            return []

        # Create (query, document) pairs
        pairs = [[query, doc.page_content] for doc in docs]

        # Predict relevance scores
        scores = self.model.predict(pairs)

        # Sort documents by score (highest first)
        scored_docs = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        # Return top_n reranked documents
        return [doc for doc, _ in scored_docs[:top_n]]
