from dataclasses import dataclass
from typing import Dict

@dataclass
class AgentConfig:
    """Configuration for multi-agent system."""

    # Model settings
    router_model: str = "llama3.1"
    research_model: str = "llama3.1"
    sql_model: str = "llama3.1"
    code_model: str = "llama3.1"
    synthesis_model: str = "llama3.1"

    # Routing thresholds
    routing_confidence_threshold: float = 0.7

    # Research agent settings
    research_top_k: int = 5

    # SQL agent settings
    sql_db_path: str = "data/sample.db"

    # Code agent settings
    code_repo_path: str = "data/code_repos"

    # Synthesis settings
    max_synthesis_tokens: int = 1000

    def to_dict(self) -> Dict:
        return {
            "router_model": self.router_model,
            "research_model": self.research_model,
            "sql_model": self.sql_model,
            "code_model": self.code_model,
            "synthesis_model": self.synthesis_model,
            "routing_confidence_threshold": self.routing_confidence_threshold,
        }