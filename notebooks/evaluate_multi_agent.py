from src.multi_agent_system import MultiAgentSystem
from src.config import AgentConfig
from src.multi_agent_tracker import MultiAgentTracker
import time

def main():
    # Test suite
    test_cases = [
        {
            "query": "What is Python?",
            "expected_type": "research",
            "description": "Basic research query"
        },
        {
            "query": "Show all users with premium plans",
            "expected_type": "sql",
            "description": "SQL data query"
        },
        {
            "query": "How does the divide function handle zero division?",
            "expected_type": "code",
            "description": "Code analysis query"
        },
        {
            "query": "What are the key features of machine learning?",
            "expected_type": "research",
            "description": "Conceptual research query"
        },
        {
            "query": "Calculate total revenue from all purchases",
            "expected_type": "sql",
            "description": "Aggregation SQL query"
        },
    ]

    print("="*60)
    print("MULTI-AGENT SYSTEM EVALUATION")
    print("="*60)

    config = AgentConfig()
    system = MultiAgentSystem(config, enable_tracking=True)

    results = []

    for i, test in enumerate(test_cases, 1):
        print(f"\n[Test {i}/{len(test_cases)}] {test['description']}")
        print(f"Query: {test['query']}")

        start_time = time.time()
        result = system.query(test['query'], verbose=False)
        execution_time = time.time() - start_time

        # Evaluate routing
        routing_correct = result['query_type'] == test['expected_type']

        results.append({
            'query': test['query'],
            'expected_type': test['expected_type'],
            'actual_type': result['query_type'],
            'routing_correct': routing_correct,
            'execution_time': execution_time,
            'answer_length': len(result.get('final_answer', '')),
            'num_sources': len(result.get('sources', [])),
            'errors': len(result['errors'])
        })

        print(f"  Expected: {test['expected_type']}")
        print(f"  Actual: {result['query_type']}")
        print(f"  Routing: {'✓' if routing_correct else '✗'}")
        print(f"  Time: {execution_time:.2f}s")

    # Summary
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)

    routing_accuracy = sum(r['routing_correct'] for r in results) / len(results)
    avg_time = sum(r['execution_time'] for r in results) / len(results)
    total_errors = sum(r['errors'] for r in results)

    print(f"Routing Accuracy: {routing_accuracy:.1%}")
    print(f"Average Execution Time: {avg_time:.2f}s")
    print(f"Total Errors: {total_errors}")
    print(f"Tests Passed: {sum(r['routing_correct'] for r in results)}/{len(results)}")

    # Save detailed results
    import json
    with open('experiments/evaluation_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n✓ Detailed results saved to experiments/evaluation_results.json")

if __name__ == "__main__":
    import os
    os.makedirs('experiments', exist_ok=True)
    main()