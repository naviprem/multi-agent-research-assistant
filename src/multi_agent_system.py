from langgraph.graph import StateGraph, END
from src.agent_state import AgentState
from src.agents.router_agent import RouterAgent
from src.agents.research_agent import ResearchAgent
from src.agents.sql_agent import SQLAgent
from src.agents.code_agent import CodeAgent
from src.agents.synthesis_agent import SynthesisAgent
from src.vector_store import VectorStoreManager
from src.config import AgentConfig
from typing import Literal, Dict
from src.multi_agent_tracker import MultiAgentTracker
from src.guardrails.guardrails_system import GuardrailsSystem

class MultiAgentSystem:
    """LangGraph-based multi-agent orchestration system."""

    def __init__(self, config: AgentConfig = None, enable_tracking: bool = True, enable_guardrails: bool = True):
        self.config = config or AgentConfig()

        self.enable_tracking = enable_tracking
        if enable_tracking:
            self.tracker = MultiAgentTracker()

        # Initialize agents
        self.router = RouterAgent(
            model=self.config.router_model,
            confidence_threshold=self.config.routing_confidence_threshold
        )

        vector_store = VectorStoreManager()
        self.research_agent = ResearchAgent(
            vector_store=vector_store,
            model=self.config.research_model,
            top_k=self.config.research_top_k
        )

        self.sql_agent = SQLAgent(
            db_path=self.config.sql_db_path,
            model=self.config.sql_model
        )

        self.code_agent = CodeAgent(
            repo_path=self.config.code_repo_path,
            model=self.config.code_model
        )

        self.synthesis_agent = SynthesisAgent(
            model=self.config.synthesis_model
        )

        self.enable_guardrails = enable_guardrails
        if enable_guardrails:
            self.guardrails = GuardrailsSystem()

        # Build graph
        self.app = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""

        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("router", self.router.route)
        workflow.add_node("research", self.research_agent.research)
        workflow.add_node("sql", self.sql_agent.query)
        workflow.add_node("code", self.code_agent.query)
        workflow.add_node("synthesis", self.synthesis_agent.synthesize)

        # Set entry point
        workflow.set_entry_point("router")

        # Add conditional routing from router
        workflow.add_conditional_edges(
            "router",
            self._route_to_specialist,
            {
                "research": "research",
                "sql": "sql",
                "code": "code",
                "general": "synthesis"
            }
        )

        # All specialists go to synthesis
        workflow.add_edge("research", "synthesis")
        workflow.add_edge("sql", "synthesis")
        workflow.add_edge("code", "synthesis")

        # Synthesis is the end
        workflow.add_edge("synthesis", END)

        return workflow.compile()

    def _route_to_specialist(self, state: AgentState) -> Literal["research", "sql", "code", "general"]:
        """Determine which specialist to route to."""
        query_type = state.get("query_type", "general")

        # Map query type to node name
        return query_type

    def query(self, user_query: str, verbose: bool = True) -> Dict:
        """Execute multi-agent query pipeline."""

        # Validate input with guardrails
        if self.enable_guardrails:
            input_validation = self.guardrails.validate_input(user_query)

            if not input_validation['is_safe']:
                return {
                    'query': user_query,
                    'final_answer': "Sorry, I cannot process this query due to safety concerns.",
                    'validation_failed': True,
                    'warnings': input_validation['warnings'],
                    'sources': [],
                    'agent_path': [],
                    'errors': input_validation['warnings']
                }

        if verbose:
            print("="*60)
            print("MULTI-AGENT SYSTEM")
            print("="*60)
            print(f"Query: {user_query}\n")
                        
        # Initialize state
        initial_state = AgentState(
            query=user_query,
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

        # Execute graph
        final_state = self.app.invoke(initial_state)

        # Track execution
        if self.enable_tracking:
            self.tracker.log_execution(
                user_query,
                final_state,
                self.config.to_dict()
            )

        if verbose:
            print("\n" + "="*60)
            print("EXECUTION SUMMARY")
            print("="*60)
            print(f"Agent Path: {' → '.join(final_state['agent_path'])}")
            print(f"Query Type: {final_state['query_type']}")
            print(f"Sources: {len(final_state.get('sources', []))}")

            if final_state['errors']:
                print(f"Errors: {final_state['errors']}")

            print("\n" + "="*60)
            print("FINAL ANSWER")
            print("="*60)
            print(final_state['final_answer'])
            print("="*60)

        # Validate output
        if self.enable_guardrails and final_state.get('final_answer'):
            contexts = [str(s) for s in final_state.get('sources', [])]
            output_validation = self.guardrails.validate_output(
                final_state['final_answer'],
                contexts
            )

            final_state['output_validation'] = output_validation

            # Sanitize if needed
            if output_validation.get('pii_in_output', {}).get('has_sensitive_pii'):
                final_state['final_answer'] = self.guardrails.sanitize_output(
                    final_state['final_answer']
                )
                
        return final_state
