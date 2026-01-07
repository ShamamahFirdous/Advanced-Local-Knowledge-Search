from pathlib import Path
from tqdm import tqdm

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


DATA_DIR = Path("data")
VECTORSTORE_DIR = Path("vectorstore")


def load_documents():
    documents = []

    for file_path in DATA_DIR.iterdir():
        if file_path.suffix in [".txt", ".md"]:
            loader = TextLoader(str(file_path))
        elif file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        elif file_path.suffix == ".csv":
            loader = CSVLoader(str(file_path))
        elif file_path.suffix == ".docx":
            loader = Docx2txtLoader(str(file_path))
        else:
            continue

        loaded_docs = loader.load()

        for i, doc in enumerate(loaded_docs):
            doc.metadata = {
                "source": "local",
                "file_type": file_path.suffix.replace(".", ""),
                "doc_name": file_path.name,
                "chunk_id": f"{file_path.stem}_{i}",
                "topic": "general",
                "year": "2024",
                "confidence_level": "medium",
            }
            documents.append(doc)

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)


if __name__ == "__main__":
    print("📥 Loading documents...")
    docs = load_documents()
    print(f"✅ Loaded {len(docs)} documents")

    print("✂️ Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"✅ Created {len(chunks)} chunks")

    print("📦 Building vectorstore...")
    build_vectorstore(chunks)

    print("🎉 Vectorstore saved successfully!")
