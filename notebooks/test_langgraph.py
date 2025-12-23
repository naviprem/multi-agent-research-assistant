from langgraph.graph import StateGraph, END
from typing import TypedDict

class GraphState(TypedDict):
    message: str
    count: int

# Simple test graph
workflow = StateGraph(GraphState)

def increment(state: GraphState) -> GraphState:
    return {"message": state["message"], "count": state["count"] + 1}

workflow.add_node("increment", increment)
workflow.set_entry_point("increment")
workflow.add_edge("increment", END)

app = workflow.compile()

# Test
result = app.invoke({"message": "test", "count": 0})
print(f"LangGraph test: {result}")
assert result["count"] == 1, "LangGraph not working correctly"
print("✓ LangGraph working correctly!")