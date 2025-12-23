"""Run Ragas evaluation on multi-agent system."""

import json
from pathlib import Path
from src.multi_agent_system import MultiAgentSystem
from src.config import AgentConfig
from src.evaluation.ragas_evaluator import RagasEvaluator


def load_test_dataset(path: str = "data/evaluation/test_dataset.json") -> list:
    """Load evaluation test cases."""
    with open(path, 'r') as f:
        data = json.load(f)
    return data['test_cases']


def run_system_on_tests(system: MultiAgentSystem, test_cases: list) -> list:
    """Execute system on all test cases."""

    results = []

    for i, test in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] Processing: {test['question']}")

        # Run system
        result = system.query(test['question'], verbose=False)

        # Add ground truth
        result['ground_truth'] = test.get('ground_truth', '')
        result['expected_type'] = test.get('expected_type')
        result['difficulty'] = test.get('difficulty', 'medium')

        results.append(result)

    return results


def main():
    print("=" * 60)
    print("RAGAS EVALUATION PIPELINE")
    print("=" * 60)

    # Load test dataset
    print("\n1. Loading test dataset...")
    test_cases = load_test_dataset()
    print(f"   Loaded {len(test_cases)} test cases")

    # Initialize system
    print("\n2. Initializing multi-agent system...")
    config = AgentConfig()
    system = MultiAgentSystem(config, enable_tracking=False)
    print("   ✓ System ready")

    # Run tests
    print("\n3. Running system on test cases...")
    results = run_system_on_tests(system, test_cases)

    # Save raw results
    output_dir = Path("experiments/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "ragas_test_results.json", 'w') as f:
        # Convert to serializable format
        serializable_results = []
        for r in results:
            serializable_results.append({
                'query': r.get('query'),
                'final_answer': r.get('final_answer'),
                'sources': [str(s) for s in r.get('sources', [])],
                'ground_truth': r.get('ground_truth'),
                'query_type': r.get('query_type')
            })
        json.dump(serializable_results, f, indent=2)

    # Run Ragas evaluation
    print("\n4. Running Ragas evaluation...")
    evaluator = RagasEvaluator()
    scores = evaluator.evaluate_system(results)

    # Generate report
    print("\n5. Generating evaluation report...")
    report = evaluator.generate_report(
        scores,
        output_path=str(output_dir / "ragas_report.txt")
    )

    print("\n" + report)

    print("\n✓ Evaluation complete!")
    print(f"Results saved to {output_dir}/")


if __name__ == "__main__":
    main()