import ollama
from typing import Dict, Optional
from src.agent_state import AgentState

class SynthesisAgent:
    """Combines outputs from multiple agents into coherent response."""

    def __init__(self, model: str = "llama3.1"):
        self.model = model

    def synthesize(self, state: AgentState) -> AgentState:
        """Synthesize final answer from agent outputs."""

        print(f"\n🔄 Synthesis Agent combining results...")

        # Gather all agent results
        results = []
        sources = []

        if state.get("research_result"):
            results.append(f"Research: {state['research_result']['answer']}")
            sources.extend(state['research_result']['sources'])

        if state.get("sql_result"):
            results.append(f"Data Analysis: {state['sql_result']['answer']}")
            sources.extend(state['sql_result']['sources'])

        if state.get("code_result"):
            results.append(f"Code Analysis: {state['code_result']['answer']}")
            sources.extend(state['code_result']['sources'])

        # If only one agent responded, use that directly
        if len(results) == 1:
            if state.get("research_result"):
                state["final_answer"] = state['research_result']['answer']
            elif state.get("sql_result"):
                state["final_answer"] = state['sql_result']['answer']
            elif state.get("code_result"):
                state["final_answer"] = state['code_result']['answer']

            state["sources"] = sources
            state["agent_path"].append("synthesis")
            return state

        # Synthesize multiple results
        combined_results = "\n\n".join(results)

        prompt = f"""You are a synthesis agent. Combine the following information from different sources into a coherent, well-structured answer to the user's question.

Original Question: {state['query']}

Information from different agents:
{combined_results}

Create a comprehensive answer that:
1. Addresses the user's question directly
2. Integrates information from all sources
3. Resolves any contradictions
4. Is clear and well-organized

Final Answer:"""

        response = ollama.generate(model=self.model, prompt=prompt)

        state["final_answer"] = response['response']
        state["sources"] = sources
        state["agent_path"].append("synthesis")

        print(f"  ✓ Synthesized answer from {len(results)} sources")

        return state