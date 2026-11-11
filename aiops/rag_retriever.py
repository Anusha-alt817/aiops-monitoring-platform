import chromadb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

def retrieve_context(query, n_results=2):
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    collection = client.get_collection(
        name="aiops_knowledge"
    )

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    retrieved_context = []

    for metadata, document, distance in zip(
        results["metadatas"][0],
        results["documents"][0],
        results["distances"][0]
    ):
        retrieved_context.append({
            "source": metadata["filename"],
            "category": metadata["category"],
            "content": document,
            "distance": distance
        })

    return retrieved_context


if __name__ == "__main__":
    question = "Why is the banking API returning HTTP 500 errors?"

    print("QUESTION:", question)

    context = retrieve_context(question)

    for item in context:
        print("\nSOURCE:", item["source"])
        print("CATEGORY:", item["category"])
        print("DISTANCE:", round(item["distance"], 4))
        print("CONTENT:\n", item["content"][:500])
