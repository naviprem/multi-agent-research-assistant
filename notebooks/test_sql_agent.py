from src.agents.sql_agent import SQLAgent
from src.agent_state import AgentState

sql_agent = SQLAgent(db_path="data/sample.db")

test_queries = [
    "Show me all premium users",
    "What are the total purchases by user?",
    "List all purchases over $100",
]

for query in test_queries:
    state = AgentState(
        query=query,
        query_type="sql",
        routing_confidence=0.9,
        research_result=None,
        sql_result=None,
        code_result=None,
        final_answer=None,
        sources=None,
        agent_path=[],
        errors=[]
    )

    result = sql_agent.query(state)

    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print(f"{'='*50}")

    if result["sql_result"]:
        print(result["sql_result"]["answer"])
    else:
        print(f"Error: {result['errors']}")