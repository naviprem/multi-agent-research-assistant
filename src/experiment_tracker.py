import mlflow
from datetime import datetime
from typing import Dict

class ExperimentTracker:
    """Track RAG experiments with MLflow."""

    def __init__(self, experiment_name: str = "rag-baseline"):
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

    def log_pipeline_run(self, config: Dict, results: Dict):
        """Log a complete RAG pipeline run."""

        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(config)

            # Log metrics
            mlflow.log_metrics({
                'num_contexts_retrieved': results.get('num_contexts', 0),
                'answer_length': len(results.get('answer', '')),
                'timestamp': datetime.now().timestamp()
            })

            # Log artifacts
            mlflow.log_text(results['question'], "question.txt")
            mlflow.log_text(results['answer'], "answer.txt")

            for i, ctx in enumerate(results.get('contexts', [])):
                mlflow.log_text(ctx, f"context_{i}.txt")

    def log_batch_evaluation(self, test_queries: list, results: list):
        """Log batch evaluation results."""

        with mlflow.start_run(run_name="batch_evaluation"):
            mlflow.log_param("num_queries", len(test_queries))

            avg_answer_length = sum(len(r['answer']) for r in results) / len(results)
            mlflow.log_metric("avg_answer_length", avg_answer_length)

            # Log all Q&A pairs
            qa_text = "\n\n".join([
                f"Q: {r['question']}\nA: {r['answer']}"
                for r in results
            ])
            mlflow.log_text(qa_text, "all_qa_pairs.txt")