"""Run multi-agent system with Phoenix tracing."""

from src.observability.traced_system import TracedMultiAgentSystem
from src.config import AgentConfig


def main():
    print("=" * 60)
    print("MULTI-AGENT SYSTEM WITH PHOENIX TRACING")
    print("=" * 60)

    config = AgentConfig()
    system = TracedMultiAgentSystem(config)

    print("\n✓ System initialized with Phoenix tracing")
    print("Visit http://localhost:6006 to view traces\n")

    test_queries = [
        "What is Python?",
        "Show all premium users",
        "How does the divide function work?"
    ]

    for query in test_queries:
        print(f"\nProcessing: {query}")
        result = system.query(query, verbose=False)
        print(f"✓ Completed in {result['execution_time']:.2f}s")

    print("\n✓ All queries processed!")
    print("Check Phoenix UI for detailed traces")

    input("\nPress Enter to stop Phoenix and exit...")
    system.close()


if __name__ == "__main__":
    main()
