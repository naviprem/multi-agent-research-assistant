"""Phoenix observability setup."""

import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor
import os


class PhoenixObservability:
    """Phoenix tracing and monitoring."""

    def __init__(self, project_name: str = "multi-agent-research"):
        self.project_name = project_name
        self.session = None

    def start_phoenix(self, port: int = 6006):
        """Start Phoenix server."""

        print("🔍 Starting Phoenix observability...")

        # Launch Phoenix
        self.session = px.launch_app(port=port)

        print(f"✓ Phoenix UI available at: http://localhost:{port}")

        return self.session

    def instrument_langchain(self):
        """Instrument LangChain for tracing."""

        # Instrument LangChain
        LangChainInstrumentor().instrument()

        print("✓ LangChain instrumentation enabled")

    def stop_phoenix(self):
        """Stop Phoenix server."""

        if self.session:
            self.session.close()
            print("✓ Phoenix server stopped")