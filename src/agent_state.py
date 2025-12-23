from typing import TypedDict, List, Dict, Optional, Literal
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    """Shared state across all agents in the graph."""

    # User input
    query: str

    # Routing information
    query_type: Optional[Literal["research", "sql", "code", "general"]]
    routing_confidence: Optional[float]

    # Agent responses
    research_result: Optional[Dict]
    sql_result: Optional[Dict]
    code_result: Optional[Dict]

    # Final output
    final_answer: Optional[str]
    sources: Optional[List[Dict]]

    # Metadata
    agent_path: List[str]  # Track which agents were invoked
    errors: List[str]


class QueryClassification(BaseModel):
    """Schema for query classification."""
    query_type: Literal["research", "sql", "code", "general"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class AgentResponse(BaseModel):
    """Standard response format for all agents."""
    answer: str
    sources: List[Dict] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Dict = Field(default_factory=dict)