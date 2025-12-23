from src.vector_store import VectorStoreManager
import ollama
from typing import List, Dict

class RAGEngine:
    """Retrieval-Augmented Generation engine."""

    def __init__(self, vector_store: VectorStoreManager, model: str = "llama3.1"):
        self.vector_store = vector_store
        self.model = model

    def retrieve_context(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant context from vector store."""
        results = self.vector_store.search(query, n_results=n_results)

        # Extract documents
        contexts = results['documents'][0] if results['documents'] else []
        return contexts

    def generate_answer(self, query: str, contexts: List[str]) -> str:
        """Generate answer using LLM with retrieved context."""

        # Build prompt
        context_str = "\n\n".join([f"[Context {i+1}]\n{ctx}" for i, ctx in enumerate(contexts)])

        prompt = f"""You are a helpful research assistant. Answer the question based ONLY on the provided context. If the context doesn't contain enough information to answer the question, say "I don't have enough information to answer that question."

Context:
{context_str}

Question: {query}

Answer:"""

        # Generate response
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']

    def query(self, question: str, n_contexts: int = 3, verbose: bool = False) -> Dict:
        """Execute RAG query pipeline."""

        # Retrieve
        if verbose:
            print(f"\n🔍 Searching for relevant context...")
        contexts = self.retrieve_context(question, n_results=n_contexts)

        if verbose:
            print(f"✓ Retrieved {len(contexts)} relevant chunks")
            for i, ctx in enumerate(contexts):
                print(f"\n[Context {i+1}]")
                print(ctx[:200] + "..." if len(ctx) > 200 else ctx)

        # Generate
        if verbose:
            print(f"\n🤖 Generating answer...")
        answer = self.generate_answer(question, contexts)

        return {
            'question': question,
            'answer': answer,
            'contexts': contexts,
            'num_contexts': len(contexts)
        }