import chromadb
from chromadb.config import Settings
from typing import List, Dict
import ollama

class VectorStoreManager:
    """Manage embeddings and vector database operations."""

    def __init__(self, collection_name: str = "documents", persist_dir: str = "./data/chroma_db"):
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Research assistant document store"}
        )

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Ollama."""
        response = ollama.embeddings(model="llama3.1", prompt=text)
        return response['embedding']

    def add_chunks(self, chunks: List[Dict]) -> None:
        """Add document chunks to vector store."""
        print(f"Generating embeddings for {len(chunks)} chunks...")

        documents = []
        embeddings = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = self.generate_embedding(chunk['text'])

            # Prepare data
            documents.append(chunk['text'])
            embeddings.append(embedding)
            metadatas.append(chunk['metadata'])
            ids.append(f"chunk_{i}")

            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(chunks)} chunks")

        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Added {len(chunks)} chunks to vector store")

    def search(self, query: str, n_results: int = 5) -> Dict:
        """Search for relevant chunks."""
        query_embedding = self.generate_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def get_stats(self) -> Dict:
        """Get collection statistics."""
        return {
            'total_chunks': self.collection.count(),
            'collection_name': self.collection_name
        }