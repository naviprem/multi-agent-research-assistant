"""Detect hallucinations in generated responses."""

import ollama
from typing import Dict, List
import json


class HallucinationDetector:
    """Detect factual inconsistencies and hallucinations."""

    def __init__(self, model: str = "llama3.1"):
        self.model = model

    def check_context_consistency(
        self,
        answer: str,
        contexts: List[str]
    ) -> Dict:
        """Check if answer is consistent with provided contexts."""

        context_str = "\n\n".join(contexts[:3])  # Use top 3 contexts

        prompt = f"""You are a fact-checking system. Determine if the answer is fully supported by the provided context.

Context:
{context_str}

Answer to check:
{answer}

Analyze if the answer contains information NOT present in the context (hallucinations).

Respond with JSON only:
{{
    "is_consistent": true/false,
    "consistency_score": 0.0-1.0,
    "hallucinated_claims": ["list", "of", "unsupported", "claims"],
    "reasoning": "brief explanation"
}}
"""

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format="json"
        )

        try:
            result = json.loads(response['response'])
            return result
        except Exception as e:
            return {
                'is_consistent': True,  # Default to safe
                'consistency_score': 0.5,
                'hallucinated_claims': [],
                'reasoning': f"Detection error: {str(e)}"
            }

    def detect_unsupported_claims(
        self,
        answer: str,
        contexts: List[str]
    ) -> List[str]:
        """Identify specific unsupported claims."""

        result = self.check_context_consistency(answer, contexts)
        return result.get('hallucinated_claims', [])

    def is_hallucination_free(
        self,
        answer: str,
        contexts: List[str],
        threshold: float = 0.7
    ) -> bool:
        """Check if answer is free from hallucinations."""

        result = self.check_context_consistency(answer, contexts)
        return result.get('consistency_score', 0) >= threshold