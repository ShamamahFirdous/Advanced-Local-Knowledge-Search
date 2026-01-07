from pathlib import Path
from typing import Dict, Any, List

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.documents import Document


VECTORSTORE_DIR = Path("vectorstore")


class AdvancedRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )

        self.vectorstore = FAISS.load_local(
            VECTORSTORE_DIR,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def retrieve(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20,
        metadata_filter: Dict[str, Any] | None = None,
    ) -> List[Document]:

        search_kwargs = {
            "k": k,
            "fetch_k": fetch_k,
        }

        if metadata_filter:
            search_kwargs["filter"] = metadata_filter

        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs=search_kwargs,
        )

        # ✅ NEW LANGCHAIN API (THIS FIXES THE ERROR)
        return retriever.invoke(query)
