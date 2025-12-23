"""Traced version of multi-agent system."""

from src.multi_agent_system import MultiAgentSystem
from src.config import AgentConfig
from src.observability.phoenix_setup import PhoenixObservability
from typing import Dict
import time


class TracedMultiAgentSystem:
    """Multi-agent system with Phoenix tracing."""

    def __init__(self, config: AgentConfig = None):
        # Initialize Phoenix
        self.phoenix = PhoenixObservability()
        self.phoenix.start_phoenix()
        self.phoenix.instrument_langchain()

        # Initialize system
        self.system = MultiAgentSystem(config)

    def query(self, user_query: str, verbose: bool = True) -> Dict:
        """Execute query with tracing."""

        start_time = time.time()

        # Execute with automatic tracing
        result = self.system.query(user_query, verbose=verbose)

        execution_time = time.time() - start_time
        result['execution_time'] = execution_time

        return result

    def close(self):
        """Clean up resources."""
        self.phoenix.stop_phoenix()