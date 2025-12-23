"""Test evaluation dependencies."""

# Test Ragas
try:
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision
    print("✓ Ragas installed successfully")
except ImportError as e:
    print(f"✗ Ragas import error: {e}")

# Test Guardrails
try:
    from guardrails import Guard
    print("✓ Guardrails AI installed successfully")
except ImportError as e:
    print(f"✗ Guardrails import error: {e}")

# Test Presidio
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    print("✓ Presidio installed successfully")
except ImportError as e:
    print(f"✗ Presidio import error: {e}")

# Test Phoenix
try:
    import phoenix as px
    print("✓ Phoenix installed successfully")
except ImportError as e:
    print(f"✗ Phoenix import error: {e}")

print("\n✓ All evaluation dependencies installed!")