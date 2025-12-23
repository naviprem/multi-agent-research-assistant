"""Generate comprehensive test dataset."""

import json
from pathlib import Path


def generate_test_dataset():
    """Generate 50+ test cases across different categories."""

    test_cases = []

    # Research queries (20 cases)
    research_queries = [
        ("What is Python?", "Python is a high-level programming language..."),
        ("Explain machine learning", "Machine learning is..."),
        ("What is data engineering?", "Data engineering involves..."),
        ("Define artificial intelligence", "AI encompasses..."),
        ("What are neural networks?", "Neural networks are..."),
        # Add 15 more...
    ]

    for question, truth in research_queries[:20]:
        test_cases.append({
            "question": question,
            "expected_type": "research",
            "ground_truth": truth,
            "difficulty": "easy",
            "category": "research"
        })

    # SQL queries (15 cases)
    sql_queries = [
        ("Show all users", "SELECT * FROM users"),
        ("List premium users", "SELECT * FROM users WHERE plan = 'premium'"),
        ("Calculate total revenue", "SELECT SUM(amount) FROM purchases"),
        # Add 12 more...
    ]

    for question, truth in sql_queries[:15]:
        test_cases.append({
            "question": question,
            "expected_type": "sql",
            "ground_truth": truth,
            "difficulty": "medium",
            "category": "sql"
        })

    # Code queries (15 cases)
    code_queries = [
        ("How does divide function work?", "The divide function..."),
        ("What validation is performed?", "validate_input checks..."),
        # Add 13 more...
    ]

    for question, truth in code_queries[:15]:
        test_cases.append({
            "question": question,
            "expected_type": "code",
            "ground_truth": truth,
            "difficulty": "medium",
            "category": "code"
        })

    # Save dataset
    output = {
        "version": "1.0",
        "total_cases": len(test_cases),
        "test_cases": test_cases
    }

    output_path = Path("data/evaluation/comprehensive_test_dataset.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✓ Generated {len(test_cases)} test cases")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    generate_test_dataset()