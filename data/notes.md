# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with large language models.
Instead of relying only on a model’s internal parameters, RAG systems retrieve relevant documents and use them as context
when generating answers.

## Why RAG is Important
Large language models can hallucinate facts when they do not have access to external knowledge.
RAG helps reduce hallucinations by grounding responses in real documents.

## Core Components of RAG
A typical RAG pipeline includes:
- Document loaders
- Text chunking
- Vector embeddings
- Similarity search
- Language model generation

## Limitations of RAG
RAG systems depend heavily on retrieval quality.
If the wrong documents are retrieved, the generated answer will still be incorrect.

## Advanced Retrieval
Advanced RAG systems use techniques like metadata filtering, Maximal Marginal Relevance (MMR),
and reranking to improve retrieval quality.
