"""Unified guardrails system."""

from typing import Dict, List
from src.guardrails.pii_detector import PIIDetector
from src.guardrails.prompt_injection_detector import PromptInjectionDetector
from src.guardrails.hallucination_detector import HallucinationDetector


class GuardrailsSystem:
    """Comprehensive guardrails for input/output validation."""

    def __init__(self):
        self.pii_detector = PIIDetector()
        self.injection_detector = PromptInjectionDetector()
        self.hallucination_detector = HallucinationDetector()

    def validate_input(self, query: str) -> Dict:
        """Validate user input before processing."""

        print("🛡️  Validating input...")

        # Check for PII
        pii_summary = self.pii_detector.get_pii_summary(query)

        # Check for prompt injection
        injection_result = self.injection_detector.detect(query)

        # Determine if input is safe
        is_safe = (
            not pii_summary['has_sensitive_pii'] and
            injection_result['risk_score'] < 0.5
        )

        validation_result = {
            'is_safe': is_safe,
            'pii_detected': pii_summary,
            'injection_detected': injection_result,
            'warnings': []
        }

        # Add warnings
        if pii_summary['has_sensitive_pii']:
            validation_result['warnings'].append("Sensitive PII detected in query")

        if injection_result['is_injection']:
            validation_result['warnings'].append(
                f"Potential prompt injection detected ({injection_result['match_count']} matches)"
            )

        # Log results
        if validation_result['warnings']:
            for warning in validation_result['warnings']:
                print(f"  ⚠️  {warning}")
        else:
            print("  ✓ Input validation passed")

        return validation_result

    def validate_output(self, answer: str, contexts: List[str]) -> Dict:
        """Validate system output before returning to user."""

        print("🛡️  Validating output...")

        # Check for hallucinations
        consistency_result = self.hallucination_detector.check_context_consistency(
            answer, contexts
        )

        # Check for PII in output
        pii_summary = self.pii_detector.get_pii_summary(answer)

        is_safe = (
            consistency_result.get('consistency_score', 0) >= 0.6 and
            not pii_summary['has_sensitive_pii']
        )

        validation_result = {
            'is_safe': is_safe,
            'consistency_check': consistency_result,
            'pii_in_output': pii_summary,
            'warnings': []
        }

        # Add warnings
        if not consistency_result.get('is_consistent', True):
            validation_result['warnings'].append("Potential hallucinations detected")

        if pii_summary['has_sensitive_pii']:
            validation_result['warnings'].append("Sensitive PII in output")

        # Log results
        if validation_result['warnings']:
            for warning in validation_result['warnings']:
                print(f"  ⚠️  {warning}")
        else:
            print("  ✓ Output validation passed")

        return validation_result

    def sanitize_output(self, answer: str) -> str:
        """Sanitize output by removing/anonymizing PII."""

        return self.pii_detector.anonymize_text(answer)