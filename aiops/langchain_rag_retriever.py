from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"


class ChromaDefaultEmbeddings(Embeddings):
    """Use ChromaDB's existing default embedding model through LangChain."""

    def __init__(self):
        self.embedding_function = DefaultEmbeddingFunction()

    def embed_documents(self, texts):
        return self.embedding_function(texts)

    def embed_query(self, text):
        return self.embedding_function([text])[0]


def create_retriever():
    embeddings = ChromaDefaultEmbeddings()

    vector_store = Chroma(
        collection_name="aiops_knowledge",
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


def main():
    question = "What should be investigated when API P95 latency is unavailable?"

    retriever = create_retriever()
    documents = retriever.invoke(question)

    print("\nQUESTION:", question)
    print("\nLANGCHAIN RETRIEVED DOCUMENTS:", len(documents))

    for document in documents:
        print("\nSOURCE:", document.metadata.get("filename"))
        print("CATEGORY:", document.metadata.get("category"))
        print("CONTENT:\n", document.page_content[:500])


if __name__ == "__main__":
    main()
