"""Run LLM-as-Judge evaluation."""

import json
from pathlib import Path
from src.evaluation.llm_judge import LLMJudge


def main():
    print("=" * 60)
    print("LLM-AS-JUDGE EVALUATION")
    print("=" * 60)

    # Load test results from Ragas evaluation
    results_path = Path("experiments/evaluation/ragas_test_results.json")

    if not results_path.exists():
        print("\nError: No test results found!")
        print("Run 'python scripts/run_ragas_evaluation.py' first")
        return

    with open(results_path, 'r') as f:
        test_results = json.load(f)

    print(f"\nLoaded {len(test_results)} test results")

    # Run LLM judge
    print("\nRunning LLM-as-Judge evaluation...")
    judge = LLMJudge(model="llama3.1")
    judged_results = judge.judge_batch(test_results)

    # Generate summary
    summary = judge.generate_summary(judged_results)

    # Save results
    output_dir = Path("experiments/evaluation")

    with open(output_dir / "llm_judge_results.json", 'w') as f:
        json.dump(judged_results, f, indent=2)

    with open(output_dir / "llm_judge_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print("\nAverage Scores (0-10):")
    for metric, score in summary.items():
        if metric.startswith('avg_'):
            print(f"  {metric[4:].capitalize()}: {score:.2f}")

    print("\nScore Distribution:")
    for category, count in summary['score_distribution'].items():
        print(f"  {category}: {count}")

    if summary.get('common_issues'):
        print("\nMost Common Issues:")
        for issue, count in summary['common_issues'].items():
            print(f"  {issue}: {count}")

    print("\n✓ Evaluation complete!")
    print(f"Detailed results: {output_dir}/llm_judge_results.json")


if __name__ == "__main__":
    main()
