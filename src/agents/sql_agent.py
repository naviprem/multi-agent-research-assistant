import sqlite3
import ollama
import json
from typing import Dict, List, Optional
from src.agent_state import AgentState, AgentResponse

class SQLAgent:
    """Agent for querying structured databases."""

    def __init__(self, db_path: str, model: str = "llama3.1"):
        self.db_path = db_path
        self.model = model
        self.schema = self._get_schema()

    def _get_schema(self) -> str:
        """Get database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        conn.close()

        return "\n\n".join([table[0] for table in tables])

    def generate_sql(self, query: str) -> str:
        """Generate SQL query from natural language."""

        prompt = f"""You are a SQL expert. Convert the natural language question into a SQL query.

Database Schema:
{self.schema}

Question: {query}

Generate ONLY the SQL query, no explanations. Use proper SQLite syntax.
SQL Query:"""

        response = ollama.generate(model=self.model, prompt=prompt)

        # Extract SQL (handle cases where LLM adds explanations)
        sql = response['response'].strip()

        # Clean up common prefixes
        for prefix in ["```sql", "```", "SQL:"]:
            if sql.startswith(prefix):
                sql = sql[len(prefix):].strip()

        if sql.endswith("```"):
            sql = sql[:-3].strip()

        return sql

    def execute_sql(self, sql: str) -> List[Dict]:
        """Execute SQL and return results."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Convert to list of dicts
            results = [dict(row) for row in rows]

            conn.close()
            return results

        except Exception as e:
            conn.close()
            raise Exception(f"SQL execution error: {str(e)}")

    def format_results(self, results: List[Dict]) -> str:
        """Format SQL results as readable text."""
        if not results:
            return "No results found."

        # Simple table format
        output = []
        output.append(f"Found {len(results)} results:\n")

        for i, row in enumerate(results[:10], 1):  # Limit to 10 rows
            output.append(f"{i}. {row}")

        if len(results) > 10:
            output.append(f"\n... and {len(results) - 10} more rows")

        return "\n".join(output)

    def query(self, state: AgentState) -> AgentState:
        """Execute SQL query pipeline."""

        print(f"\n🗄️  SQL Agent processing query...")

        try:
            # Generate SQL
            sql = self.generate_sql(state["query"])
            print(f"  Generated SQL: {sql}")

            # Execute
            results = self.execute_sql(sql)
            print(f"  Returned {len(results)} rows")

            # Format
            formatted = self.format_results(results)

            response = AgentResponse(
                answer=formatted,
                sources=[{"type": "sql_query", "content": sql}],
                confidence=0.85,
                metadata={"sql": sql, "row_count": len(results)}
            )

            state["sql_result"] = response.model_dump()
            state["agent_path"].append("sql")

        except Exception as e:
            error_msg = f"SQL Agent error: {str(e)}"
            print(f"  ❌ {error_msg}")
            state["errors"].append(error_msg)

        return state