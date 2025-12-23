import mlflow
from datetime import datetime
from typing import Dict
from src.agent_state import AgentState

class MultiAgentTracker:
    """Track multi-agent system experiments."""

    def __init__(self, experiment_name: str = "multi-agent-system"):
        mlflow.set_experiment(experiment_name)

    def log_execution(self, query: str, result: AgentState, config: Dict):
        """Log a complete multi-agent execution."""

        with mlflow.start_run():
            # Log configuration
            mlflow.log_params(config)

            # Log query metadata
            mlflow.log_param("query", query[:100])  # Truncate long queries
            mlflow.log_param("query_type", result.get("query_type"))
            mlflow.log_param("routing_confidence", result.get("routing_confidence"))

            # Log execution path
            mlflow.log_param("agent_path", " → ".join(result["agent_path"]))
            mlflow.log_param("num_agents", len(result["agent_path"]))

            # Log metrics
            mlflow.log_metric("answer_length", len(result.get("final_answer", "")))
            mlflow.log_metric("num_sources", len(result.get("sources", [])))
            mlflow.log_metric("num_errors", len(result["errors"]))
            mlflow.log_metric("timestamp", datetime.now().timestamp())

            # Log artifacts
            mlflow.log_text(query, "query.txt")
            mlflow.log_text(result.get("final_answer", ""), "answer.txt")

            if result.get("sources"):
                sources_text = "\n\n".join([
                    f"Source {i+1}: {src}"
                    for i, src in enumerate(result["sources"])
                ])
                mlflow.log_text(sources_text, "sources.txt")

            if result["errors"]:
                mlflow.log_text("\n".join(result["errors"]), "errors.txt")