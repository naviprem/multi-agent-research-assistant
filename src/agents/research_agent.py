from src.vector_store import VectorStoreManager
from src.agent_state import AgentState, AgentResponse
import ollama
from typing import List, Dict

class ResearchAgent:
    """RAG-based research agent for document retrieval."""

    def __init__(self, vector_store: VectorStoreManager, model: str = "llama3.1", top_k: int = 5):
        self.vector_store = vector_store
        self.model = model
        self.top_k = top_k

    def retrieve_context(self, query: str) -> List[str]:
        """Retrieve relevant documents."""
        results = self.vector_store.search(query, n_results=self.top_k)
        return results['documents'][0] if results['documents'] else []

    def generate_answer(self, query: str, contexts: List[str]) -> AgentResponse:
        """Generate answer from retrieved context."""

        context_str = "\n\n".join([
            f"[Document {i+1}]\n{ctx}"
            for i, ctx in enumerate(contexts)
        ])

        prompt = f"""You are a research assistant. Answer the question based on the provided documents.
If the documents don't contain enough information, say so clearly.

Documents:
{context_str}

Question: {query}

Provide a detailed, well-structured answer."""

        response = ollama.generate(model=self.model, prompt=prompt)

        # Extract sources
        sources = [
            {"type": "document", "content": ctx[:200] + "..."}
            for ctx in contexts
        ]

        return AgentResponse(
            answer=response['response'],
            sources=sources,
            confidence=0.8,  # Can be improved with evaluation
            metadata={"num_sources": len(contexts)}
        )

    def research(self, state: AgentState) -> AgentState:
        """Execute research pipeline."""

        print(f"\n📚 Research Agent processing query...")

        # Retrieve
        contexts = self.retrieve_context(state["query"])
        print(f"  Retrieved {len(contexts)} relevant documents")

        # Generate
        result = self.generate_answer(state["query"], contexts)
        print(f"  Generated answer with confidence: {result.confidence:.2f}")

        # Update state
        state["research_result"] = result.model_dump()
        state["agent_path"].append("research")

        return state