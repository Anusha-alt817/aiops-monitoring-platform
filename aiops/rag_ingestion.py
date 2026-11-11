from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

def ingest_documents():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    embedding_function = DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="aiops_knowledge",
        embedding_function=embedding_function,
        metadata={"description": "AIOps incidents and troubleshooting runbooks"}
    )

    documents = []
    metadatas = []
    ids = []

    for folder in ["incidents", "runbooks"]:
        folder_path = KNOWLEDGE_BASE / folder

        for file_path in folder_path.glob("*.md"):
            content = file_path.read_text(encoding="utf-8").strip()

            if not content:
                continue

            documents.append(content)
            metadatas.append({
                "source": str(file_path.relative_to(PROJECT_ROOT)),
                "category": folder,
                "filename": file_path.name
            })
            ids.append(str(file_path.relative_to(KNOWLEDGE_BASE)))

    if not documents:
        print("No knowledge-base documents found.")
        return

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Successfully ingested {len(documents)} documents.")

    for metadata in metadatas:
        print(f"- {metadata['category']}: {metadata['filename']}")

    print(f"Total documents in ChromaDB: {collection.count()}")

if __name__ == "__main__":
    ingest_documents()
