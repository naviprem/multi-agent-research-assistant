from src.vector_store import VectorStoreManager
from src.rag_engine import RAGEngine

def main():
    print("=" * 50)
    print("RAG Query System")
    print("=" * 50)

    # Initialize
    print("\nInitializing vector store and RAG engine...")
    vector_store = VectorStoreManager()
    rag_engine = RAGEngine(vector_store)

    stats = vector_store.get_stats()
    print(f"✓ Loaded vector store with {stats['total_chunks']} chunks\n")

    print("Enter your questions (or 'quit' to exit):\n")

    while True:
        query = input("Question: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        # Execute query
        result = rag_engine.query(query, verbose=True)

        print(f"\n{'='*50}")
        print(f"ANSWER:")
        print(f"{'='*50}")
        print(result['answer'])
        print(f"\n{'='*50}\n")

if __name__ == "__main__":
    main()