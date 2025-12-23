from src.multi_agent_system import MultiAgentSystem
from src.config import AgentConfig

def main():
    print("Initializing Multi-Agent System...")

    config = AgentConfig()
    system = MultiAgentSystem(config)

    print("✓ System ready!\n")
    print("Enter your queries (or 'quit' to exit):\n")

    while True:
        query = input("Query: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            result = system.query(query, verbose=True)
        except Exception as e:
            print(f"Error: {str(e)}")

        print("\n")

if __name__ == "__main__":
    main()