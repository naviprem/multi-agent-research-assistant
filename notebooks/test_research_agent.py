from src.agents.research_agent import ResearchAgent
from src.vector_store import VectorStoreManager
from src.agent_state import AgentState

# Initialize
vector_store = VectorStoreManager()
research_agent = ResearchAgent(vector_store)

# Test query
state = AgentState(
    query="What is Python and what are its key features?",
    query_type="research",
    routing_confidence=0.9,
    research_result=None,
    sql_result=None,
    code_result=None,
    final_answer=None,
    sources=None,
    agent_path=[],
    errors=[]
)

result = research_agent.research(state)

print("\n" + "="*50)
print("RESEARCH RESULT:")
print("="*50)
print(result["research_result"]["answer"])
print(f"\nSources: {len(result['research_result']['sources'])}")