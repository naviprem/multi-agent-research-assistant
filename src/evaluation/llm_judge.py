"""LLM-as-Judge evaluation system."""

import ollama
import json
from typing import Dict, List
from pydantic import BaseModel, Field


class JudgeScore(BaseModel):
    """Structured output for judge scoring."""

    accuracy: float = Field(ge=0.0, le=10.0, description="Factual accuracy (0-10)")
    relevance: float = Field(ge=0.0, le=10.0, description="Relevance to question (0-10)")
    completeness: float = Field(ge=0.0, le=10.0, description="Completeness of answer (0-10)")
    clarity: float = Field(ge=0.0, le=10.0, description="Clarity and coherence (0-10)")
    overall: float = Field(ge=0.0, le=10.0, description="Overall quality (0-10)")
    reasoning: str = Field(description="Explanation for the scores")
    issues: List[str] = Field(default_factory=list, description="List of issues found")


class LLMJudge:
    """Use LLM to judge response quality."""

    def __init__(self, model: str = "llama3.1"):
        self.model = model

    def judge_response(
        self,
        question: str,
        answer: str,
        context: str = None,
        ground_truth: str = None
    ) -> JudgeScore:
        """Judge a single response."""

        prompt = f"""You are an expert evaluator assessing the quality of AI-generated responses.

Question: {question}

Generated Answer: {answer}
"""

        if ground_truth:
            prompt += f"\nExpected Answer (Ground Truth): {ground_truth}\n"

        if context:
            prompt += f"\nProvided Context: {context}\n"

        prompt += """
Evaluate the answer on these criteria (0-10 scale):

1. Accuracy: Is the answer factually correct?
2. Relevance: Does it address the question asked?
3. Completeness: Does it fully answer the question?
4. Clarity: Is it clear and well-structured?
5. Overall: Overall quality assessment

Respond with JSON only:
{
    "accuracy": 0-10,
    "relevance": 0-10,
    "completeness": 0-10,
    "clarity": 0-10,
    "overall": 0-10,
    "reasoning": "brief explanation",
    "issues": ["list", "of", "issues"]
}
"""

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format="json"
        )

        try:
            result = json.loads(response['response'])
            return JudgeScore(**result)
        except Exception as e:
            # Return default scores on error
            return JudgeScore(
                accuracy=5.0,
                relevance=5.0,
                completeness=5.0,
                clarity=5.0,
                overall=5.0,
                reasoning=f"Evaluation error: {str(e)}",
                issues=["evaluation_failed"]
            )

    def judge_batch(self, test_results: List[Dict]) -> List[Dict]:
        """Judge multiple responses."""

        judged_results = []

        for i, result in enumerate(test_results, 1):
            print(f"  Judging response {i}/{len(test_results)}...")

            # Extract context
            context = ""
            if result.get('sources'):
                context = "\n".join([
                    str(s.get('content', s)) if isinstance(s, dict) else str(s)
                    for s in result['sources'][:3]  # Use top 3 sources
                ])

            # Judge
            scores = self.judge_response(
                question=result.get('query', ''),
                answer=result.get('final_answer', ''),
                context=context[:1000],  # Limit context length
                ground_truth=result.get('ground_truth')
            )

            judged_results.append({
                'query': result.get('query'),
                'answer': result.get('final_answer'),
                'scores': scores.model_dump(),
                'query_type': result.get('query_type')
            })

        return judged_results

    def generate_summary(self, judged_results: List[Dict]) -> Dict:
        """Generate summary statistics from judged results."""

        if not judged_results:
            return {}

        # Aggregate scores
        metrics = ['accuracy', 'relevance', 'completeness', 'clarity', 'overall']
        aggregates = {metric: [] for metric in metrics}

        for result in judged_results:
            scores = result['scores']
            for metric in metrics:
                aggregates[metric].append(scores[metric])

        # Calculate averages
        summary = {
            f'avg_{metric}': sum(values) / len(values)
            for metric, values in aggregates.items()
        }

        # Add distribution
        summary['score_distribution'] = {
            'excellent (8-10)': sum(1 for r in judged_results if r['scores']['overall'] >= 8),
            'good (6-8)': sum(1 for r in judged_results if 6 <= r['scores']['overall'] < 8),
            'fair (4-6)': sum(1 for r in judged_results if 4 <= r['scores']['overall'] < 6),
            'poor (0-4)': sum(1 for r in judged_results if r['scores']['overall'] < 4)
        }

        # Count common issues
        all_issues = []
        for result in judged_results:
            all_issues.extend(result['scores'].get('issues', []))

        from collections import Counter
        summary['common_issues'] = dict(Counter(all_issues).most_common(5))

        return summary


