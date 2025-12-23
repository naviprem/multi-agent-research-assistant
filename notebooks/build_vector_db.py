from src.document_loader import DocumentLoader
from src.chunker import SemanticChunker
from src.vector_store import VectorStoreManager

def main():
    print("=" * 50)
    print("Building Vector Database")
    print("=" * 50)

    # Load documents
    print("\n1. Loading documents...")
    loader = DocumentLoader()
    docs = loader.load_all()
    print(f"Loaded {len(docs)} documents")

    # Chunk documents
    print("\n2. Chunking documents...")
    chunker = SemanticChunker(chunk_size=512, chunk_overlap=50)
    chunks = chunker.chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    # Create vector store
    print("\n3. Creating vector store and generating embeddings...")
    vector_store = VectorStoreManager()
    vector_store.add_chunks(chunks)

    # Show stats
    print("\n4. Vector store statistics:")
    stats = vector_store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✓ Vector database built successfully!")

if __name__ == "__main__":
    main()