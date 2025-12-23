import os
from pathlib import Path
from typing import List, Dict
import ollama
from src.agent_state import AgentState, AgentResponse

class CodeAgent:
    """Agent for analyzing code repositories."""

    def __init__(self, repo_path: str, model: str = "llama3.1"):
        self.repo_path = Path(repo_path)
        self.model = model
        self.code_extensions = {'.py', '.js', '.java', '.cpp', '.go', '.rs'}

    def search_code(self, query: str) -> List[Dict]:
        """Search for relevant code files."""
        results = []

        # Simple keyword search
        query_lower = query.lower()

        for filepath in self.repo_path.rglob('*'):
            if filepath.is_file() and filepath.suffix in self.code_extensions:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Check if query keywords appear in file
                        if any(keyword in content.lower() for keyword in query_lower.split()):
                            results.append({
                                'filepath': str(filepath),
                                'content': content,
                                'size': len(content)
                            })
                except Exception:
                    continue

        return results[:5]  # Return top 5 matches

    def analyze_code(self, query: str, code_files: List[Dict]) -> str:
        """Analyze code files using LLM."""

        code_context = "\n\n".join([
            f"File: {file['filepath']}\n```\n{file['content'][:1000]}\n```"
            for file in code_files
        ])

        prompt = f"""You are a code analysis expert. Answer the question about the code.

Code Files:
{code_context}

Question: {query}

Provide a detailed analysis of the code related to the question."""

        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']

    def query(self, state: AgentState) -> AgentState:
        """Execute code analysis pipeline."""

        print(f"\n💻 Code Agent processing query...")

        try:
            # Search for relevant code
            code_files = self.search_code(state["query"])
            print(f"  Found {len(code_files)} relevant code files")

            if not code_files:
                state["errors"].append("No relevant code files found")
                return state

            # Analyze
            analysis = self.analyze_code(state["query"], code_files)
            print(f"  Generated code analysis")

            response = AgentResponse(
                answer=analysis,
                sources=[
                    {"type": "code_file", "content": f['filepath']}
                    for f in code_files
                ],
                confidence=0.75,
                metadata={"num_files": len(code_files)}
            )

            state["code_result"] = response.model_dump()
            state["agent_path"].append("code")

        except Exception as e:
            error_msg = f"Code Agent error: {str(e)}"
            print(f"  ❌ {error_msg}")
            state["errors"].append(error_msg)

        return state