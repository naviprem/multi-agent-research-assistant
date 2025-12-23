import ollama
import json
from typing import Dict
from src.agent_state import AgentState, QueryClassification

class RouterAgent:
    """Routes queries to appropriate specialist agents."""

    def __init__(self, model: str = "llama3.1", confidence_threshold: float = 0.7):
        self.model = model
        self.confidence_threshold = confidence_threshold

    def classify_query(self, query: str) -> QueryClassification:
        """Classify the query type using LLM."""

        prompt = f"""You are a query classification system. Analyze the user query and determine which type of agent should handle it.

Agent Types:
- research: Questions about concepts, documentation, general knowledge that require document retrieval
- sql: Questions that require querying structured data, databases, or data analysis
- code: Questions about code, programming, debugging, or code repository analysis
- general: Simple questions that don't require specialized tools

User Query: {query}

Respond with JSON only:
{{
    "query_type": "research|sql|code|general",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format="json"
        )

        try:
            result = json.loads(response['response'])
            return QueryClassification(**result)
        except Exception as e:
            # Default to research on error
            return QueryClassification(
                query_type="general",
                confidence=0.5,
                reasoning=f"Classification error: {str(e)}"
            )

    def route(self, state: AgentState) -> AgentState:
        """Route query to appropriate agent."""

        print(f"\n🔀 Router Agent analyzing query...")

        classification = self.classify_query(state["query"])

        print(f"  Query Type: {classification.query_type}")
        print(f"  Confidence: {classification.confidence:.2f}")
        print(f"  Reasoning: {classification.reasoning}")

        # Update state
        state["query_type"] = classification.query_type
        state["routing_confidence"] = classification.confidence
        state["agent_path"].append("router")

        return state

    def should_route_to_specialist(self, state: AgentState) -> bool:
        """Determine if confidence is high enough to route."""
        return state["routing_confidence"] >= self.confidence_threshold