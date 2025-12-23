from src.document_loader import DocumentLoader
from src.chunker import SemanticChunker

# Load documents
loader = DocumentLoader()
docs = loader.load_all()

# Chunk documents
chunker = SemanticChunker(chunk_size=100, chunk_overlap=5)
chunks = chunker.chunk_documents(docs)

print(f"\nCreated {len(chunks)} chunks from {len(docs)} documents")
print("\nSample chunks:")
for i, chunk in enumerate(chunks[:10]):
    print(f"\nChunk {i}:")
    print(f"Text: {chunk['text']}...")
    print(f"Metadata: {chunk['metadata']}")