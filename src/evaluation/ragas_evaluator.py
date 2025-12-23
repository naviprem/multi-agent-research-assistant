"""Ragas-based evaluation for RAG systems."""

from typing import List, Dict
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)
import pandas as pd


class RagasEvaluator:
    """Evaluate RAG system using Ragas metrics."""

    def __init__(self):
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness
        ]

    def prepare_dataset(self, test_results: List[Dict]) -> Dataset:
        """Convert test results to Ragas dataset format."""

        data = {
            'question': [],
            'answer': [],
            'contexts': [],
            'ground_truth': []
        }

        for result in test_results:
            data['question'].append(result['query'])
            data['answer'].append(result.get('final_answer', ''))

            # Extract context from sources
            contexts = []
            for source in result.get('sources', []):
                if isinstance(source, dict):
                    contexts.append(source.get('content', ''))
                else:
                    contexts.append(str(source))
            data['contexts'].append(contexts if contexts else [''])

            data['ground_truth'].append(result.get('ground_truth', ''))

        return Dataset.from_dict(data)

    def evaluate_system(self, test_results: List[Dict]) -> Dict:
        """Run Ragas evaluation on test results."""

        print("🔍 Running Ragas evaluation...")

        # Prepare dataset
        dataset = self.prepare_dataset(test_results)

        # Run evaluation
        results = evaluate(
            dataset,
            metrics=self.metrics
        )

        # Convert to dict
        scores = results.to_pandas().to_dict('records')[0]

        print("\n📊 Ragas Scores:")
        for metric, score in scores.items():
            print(f"  {metric}: {score:.3f}")

        return scores

    def evaluate_with_custom_embeddings(
        self,
        test_results: List[Dict],
        embeddings_model: str = "llama3.1"
    ) -> Dict:
        """Run evaluation with custom local embeddings."""

        # Note: Ragas typically uses OpenAI embeddings by default
        # For local setup, we'll use the default metrics which work
        # with the provided contexts and answers

        return self.evaluate_system(test_results)

    def generate_report(self, scores: Dict, output_path: str = None) -> str:
        """Generate evaluation report."""

        report = []
        report.append("=" * 60)
        report.append("RAGAS EVALUATION REPORT")
        report.append("=" * 60)
        report.append("")

        # Overall score
        avg_score = sum(scores.values()) / len(scores)
        report.append(f"Overall Score: {avg_score:.3f}")
        report.append("")

        # Individual metrics
        report.append("Metric Breakdown:")
        report.append("-" * 60)

        metric_descriptions = {
            'faithfulness': 'Measures factual consistency with context',
            'answer_relevancy': 'Measures relevance to the question',
            'context_precision': 'Measures precision of retrieved context',
            'context_recall': 'Measures recall of relevant context',
            'answer_correctness': 'Measures correctness vs ground truth'
        }

        for metric, score in scores.items():
            desc = metric_descriptions.get(metric, 'No description')
            status = "✓" if score >= 0.7 else "⚠" if score >= 0.5 else "✗"
            report.append(f"{status} {metric}: {score:.3f}")
            report.append(f"   {desc}")
            report.append("")

        # Performance assessment
        report.append("=" * 60)
        report.append("ASSESSMENT:")
        report.append("=" * 60)

        if avg_score >= 0.8:
            report.append("✓ Excellent: System meets production quality standards")
        elif avg_score >= 0.6:
            report.append("⚠ Good: System needs minor improvements")
        elif avg_score >= 0.4:
            report.append("⚠ Fair: System needs significant improvements")
        else:
            report.append("✗ Poor: System requires major redesign")

        report_text = "\n".join(report)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
            print(f"\n✓ Report saved to {output_path}")

        return report_text