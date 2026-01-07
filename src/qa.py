import sys
import time
from retriever import AdvancedRetriever
from reranker import Reranker


class GroundedQA:
    def __init__(self):
        self.retriever = AdvancedRetriever()
        self.reranker = Reranker()

    def answer(self, question: str, top_k: int = 5, verbose: bool = True):
        start_time = time.time()

        # 1️⃣ Retrieval (MMR)
        retrieved_docs = self.retriever.retrieve(
            query=question,
            k=10,
            fetch_k=25,
        )

        retrieval_time = time.time() - start_time

        # 2️⃣ Reranking
        rerank_start = time.time()
        reranked_docs = self.reranker.rerank(
            query=question,
            docs=retrieved_docs,
            top_n=top_k,
        )
        rerank_time = time.time() - rerank_start

        if not reranked_docs:
            return {
                "answer": "Insufficient information in the knowledge base.",
                "sources": [],
                "stats": {},
            }

        # 3️⃣ Build context
        context = "\n\n".join(
            f"[Source: {doc.metadata['doc_name']} | Chunk: {doc.metadata['chunk_id']}]\n{doc.page_content}"
            for doc in reranked_docs
        )

        answer = self.simple_answer(question, context)

        total_time = time.time() - start_time

        result = {
            "answer": answer,
            "sources": [
                {
                    "file": doc.metadata["doc_name"],
                    "chunk_id": doc.metadata["chunk_id"],
                    "file_type": doc.metadata["file_type"],
                }
                for doc in reranked_docs
            ],
            "stats": {
                "retrieved_chunks": len(retrieved_docs),
                "reranked_chunks": len(reranked_docs),
                "retrieval_time_sec": round(retrieval_time, 3),
                "rerank_time_sec": round(rerank_time, 3),
                "total_time_sec": round(total_time, 3),
            },
        }

        return result

    def simple_answer(self, question: str, context: str):
        keywords = question.lower().split()
        sentences = context.split(".")

        relevant = [
            s.strip()
            for s in sentences
            if any(word in s.lower() for word in keywords)
        ]

        if not relevant:
            return "Answer not found in the provided documents."

        return ". ".join(relevant[:3]) + "."


def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a question.")
        print('Usage: python src/qa.py "Your question here"')
        sys.exit(1)

    question = sys.argv[1]

    qa = GroundedQA()
    result = qa.answer(question)

    print("\n❓ Question:")
    print(question)

    print("\n✅ Answer:")
    print(result["answer"])

    print("\n📚 Sources Used:")
    for src in result["sources"]:
        print(f"- {src['file']} (chunk: {src['chunk_id']}, type: {src['file_type']})")

    print("\n📊 Retrieval Stats:")
    for k, v in result["stats"].items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
