from src.document_loader import DocumentLoader

loader = DocumentLoader()
docs = loader.load_all()

print(f"\nLoaded {len(docs)} documents:")
for doc in docs:
    print(f"- {doc['metadata']['filename']}: {len(doc['content'])} characters")