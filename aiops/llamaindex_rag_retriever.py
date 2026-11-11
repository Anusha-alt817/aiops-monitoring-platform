from pathlib import Path
import chromadb

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.embeddings import BaseEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "aiops_knowledge"


class ChromaDefaultEmbeddings(BaseEmbedding):
    def __init__(self, embedding_function):
        super().__init__()
        self._embedding_function = embedding_function

    def _get_text_embedding(self, text):
        return self._embedding_function([text])[0]

    async def _aget_text_embedding(self, text):
        return self._get_text_embedding(text)

    async def _aget_query_embedding(self, query):
        return self._get_query_embedding(query)

    def _get_query_embedding(self, query):
        return self._get_text_embedding(query)


def create_index():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction()
    )

    vector_store = ChromaVectorStore(chroma_collection=collection)

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    embedding_model = ChromaDefaultEmbeddings(
        DefaultEmbeddingFunction()
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embedding_model
    )

    return index


def main():
    print("\nLLAMAINDEX + CHROMADB RAG RETRIEVER")
    print("=" * 50)

    index = create_index()

    retriever = index.as_retriever(similarity_top_k=3)

    question = (
        "How should we investigate high API P95 latency "
        "when CPU and memory usage are normal?"
    )

    print("\nQuestion:", question)
    print("\nRetrieved historical knowledge:\n")

    results = retriever.retrieve(question)

    for number, result in enumerate(results, start=1):
        print(f"\nDocument {number}")
        print("-" * 40)
        print(result.text[:1000])
        print("Similarity score:", result.score)


if __name__ == "__main__":
    main()
