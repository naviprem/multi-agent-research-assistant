from src.agents.router_agent import RouterAgent
from src.agent_state import AgentState

router = RouterAgent()

test_queries = [
    "What is machine learning?",
    "Show me all users who purchased in the last 30 days",
    "How does the authentication function work in main.py?",
    "What's the weather like today?"
]

for query in test_queries:
    state = AgentState(
        query=query,
        query_type=None,
        routing_confidence=None,
        research_result=None,
        sql_result=None,
        code_result=None,
        final_answer=None,
        sources=None,
        agent_path=[],
        errors=[]
    )

    result = router.route(state)
    print(f"\nQuery: {query}")
    print(f"Routed to: {result['query_type']}")
    print(f"Confidence: {result['routing_confidence']:.2f}")
    print("-" * 50)