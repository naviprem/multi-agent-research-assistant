from src.vector_store import VectorStoreManager
from src.rag_engine import RAGEngine
from src.experiment_tracker import ExperimentTracker

def main():
    # Test queries
    test_queries = [
        "What is Python?",
        "Explain machine learning",
        "What are the types of machine learning?",
    ]

    # Configuration
    config = {
        'model': 'llama3.1',
        'chunk_size': 512,
        'chunk_overlap': 50,
        'n_contexts': 3
    }

    # Initialize
    vector_store = VectorStoreManager()
    rag_engine = RAGEngine(vector_store, model=config['model'])
    tracker = ExperimentTracker()

    print("Running evaluation...")
    results = []

    for query in test_queries:
        print(f"\nProcessing: {query}")
        result = rag_engine.query(query, n_contexts=config['n_contexts'])
        results.append(result)

        # Log individual run
        tracker.log_pipeline_run(config, result)

    # Log batch results
    tracker.log_batch_evaluation(test_queries, results)

    print("\n✓ Evaluation complete! Check MLflow UI for results.")
    print("Run: mlflow ui")

if __name__ == "__main__":
    main()