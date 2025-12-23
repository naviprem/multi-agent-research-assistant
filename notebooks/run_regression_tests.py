"""Run comprehensive regression test suite."""

import json
from pathlib import Path
from src.multi_agent_system import MultiAgentSystem
from src.config import AgentConfig
from src.evaluation.llm_judge import LLMJudge
import time


def run_regression_suite():
    """Run full regression test suite."""

    print("=" * 60)
    print("REGRESSION TEST SUITE")
    print("=" * 60)

    # Load test dataset
    dataset_path = Path("data/evaluation/comprehensive_test_dataset.json")

    if not dataset_path.exists():
        print("\nGenerating test dataset...")
        import subprocess
        subprocess.run(["python", "scripts/generate_test_dataset.py"])

    with open(dataset_path, 'r') as f:
        dataset = json.load(f)

    test_cases = dataset['test_cases']
    print(f"\nLoaded {len(test_cases)} test cases")

    # Initialize system
    config = AgentConfig()
    system = MultiAgentSystem(config, enable_tracking=False)
    judge = LLMJudge()

    # Run tests
    results = []
    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {test['question'][:50]}...")

        start_time = time.time()
        result = system.query(test['question'], verbose=False)
        execution_time = time.time() - start_time

        # Check routing correctness
        routing_correct = result['query_type'] == test['expected_type']

        # Get quality score
        contexts = [str(s) for s in result.get('sources', [])]
        judge_score = judge.judge_response(
            question=test['question'],
            answer=result.get('final_answer', ''),
            context="\n".join(contexts[:2]),
            ground_truth=test.get('ground_truth')
        )

        # Determine pass/fail
        test_passed = (
            routing_correct and
            judge_score.overall >= 6.0 and
            len(result['errors']) == 0
        )

        if test_passed:
            passed += 1
        else:
            failed += 1

        results.append({
            'test_id': i,
            'question': test['question'],
            'category': test['category'],
            'expected_type': test['expected_type'],
            'actual_type': result['query_type'],
            'routing_correct': routing_correct,
            'quality_score': judge_score.overall,
            'execution_time': execution_time,
            'passed': test_passed,
            'errors': result['errors']
        })

    # Save results
    output_dir = Path("experiments/regression")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "regression_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # Generate report
    print("\n" + "=" * 60)
    print("REGRESSION TEST REPORT")
    print("=" * 60)
    print(f"\nTotal Tests: {len(test_cases)}")
    print(f"Passed: {passed} ({passed/len(test_cases)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/len(test_cases)*100:.1f}%)")

    # Breakdown by category
    categories = {}
    for result in results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = {'passed': 0, 'total': 0}
        categories[cat]['total'] += 1
        if result['passed']:
            categories[cat]['passed'] += 1

    print("\nResults by Category:")
    for cat, stats in categories.items():
        pass_rate = stats['passed'] / stats['total'] * 100
        print(f"  {cat}: {stats['passed']}/{stats['total']} ({pass_rate:.1f}%)")

    print(f"\n✓ Results saved to {output_dir}/regression_results.json")


if __name__ == "__main__":
    run_regression_suite()