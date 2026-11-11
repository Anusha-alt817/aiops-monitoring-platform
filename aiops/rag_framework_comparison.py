from langchain_rag_retriever import create_retriever
from llamaindex_rag_retriever import create_index

QUESTION = (
    "What should be investigated when API P95 latency "
    "is unavailable?"
)


def run_comparison():
    print("\nRAG FRAMEWORK COMPARISON")
    print("=" * 60)
    print("Question:", QUESTION)

    # LangChain retrieval
    langchain_retriever = create_retriever()
    langchain_docs = langchain_retriever.invoke(QUESTION)

    print("\nLANGCHAIN RESULTS")
    print("-" * 60)

    for number, doc in enumerate(langchain_docs, start=1):
        print(
            f"{number}. "
            f"{doc.metadata.get('filename', 'Unknown')}"
        )

    # LlamaIndex retrieval
    llama_index = create_index()
    llama_retriever = llama_index.as_retriever(
        similarity_top_k=3
    )
    llama_docs = llama_retriever.retrieve(QUESTION)

    print("\nLLAMAINDEX RESULTS")
    print("-" * 60)

    for number, doc in enumerate(llama_docs, start=1):
        print(
            f"{number}. "
            f"{doc.metadata.get('filename', 'Unknown')}"
        )

    print("\nCOMPARISON SUMMARY")
    print("-" * 60)
    print("LangChain retrieved:", len(langchain_docs))
    print("LlamaIndex retrieved:", len(llama_docs))
    print("Shared vector database: aiops_knowledge")
    print("Shared embedding: ChromaDB DefaultEmbeddingFunction")


if __name__ == "__main__":
    run_comparison()
