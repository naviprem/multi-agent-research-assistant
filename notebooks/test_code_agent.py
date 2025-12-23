from src.agents.code_agent import CodeAgent
from src.agent_state import AgentState

code_agent = CodeAgent(repo_path="data/code_repos/sample_project")

test_queries = [
    "How does the divide function work?",
    "What validation is performed on inputs?",
    "Show me all mathematical operations available",
]

for query in test_queries:
    state = AgentState(
        query=query,
        query_type="code",
        routing_confidence=0.9,
        research_result=None,
        sql_result=None,
        code_result=None,
        final_answer=None,
        sources=None,
        agent_path=[],
        errors=[]
    )

    result = code_agent.query(state)

    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print(f"{'='*50}")

    if result["code_result"]:
        print(result["code_result"]["answer"])
    else:
        print(f"Error: {result['errors']}")