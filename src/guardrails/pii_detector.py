"""PII detection and anonymization."""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import Dict, List
import spacy


class PIIDetector:
    """Detect and anonymize PII in text."""

    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

        # Try to load spacy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not loaded. Run: python -m spacy download en_core_web_sm")
            self.nlp = None

    def detect_pii(self, text: str) -> List[Dict]:
        """Detect PII entities in text."""

        results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=[
                "PERSON",
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",
                "CREDIT_CARD",
                "US_SSN",
                "LOCATION",
                "DATE_TIME",
                "IP_ADDRESS",
                "URL"
            ]
        )

        return [
            {
                'type': result.entity_type,
                'start': result.start,
                'end': result.end,
                'score': result.score,
                'text': text[result.start:result.end]
            }
            for result in results
        ]

    def anonymize_text(self, text: str) -> str:
        """Anonymize PII in text."""

        analyzer_results = self.analyzer.analyze(
            text=text,
            language='en'
        )

        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results
        )

        return anonymized_result.text

    def has_sensitive_pii(self, text: str, threshold: float = 0.8) -> bool:
        """Check if text contains high-confidence PII."""

        pii_entities = self.detect_pii(text)

        # Filter for sensitive PII types
        sensitive_types = {
            "CREDIT_CARD",
            "US_SSN",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER"
        }

        for entity in pii_entities:
            if entity['type'] in sensitive_types and entity['score'] >= threshold:
                return True

        return False

    def get_pii_summary(self, text: str) -> Dict:
        """Get summary of PII found in text."""

        pii_entities = self.detect_pii(text)

        summary = {
            'total_pii_found': len(pii_entities),
            'has_sensitive_pii': self.has_sensitive_pii(text),
            'pii_by_type': {}
        }

        for entity in pii_entities:
            pii_type = entity['type']
            if pii_type not in summary['pii_by_type']:
                summary['pii_by_type'][pii_type] = 0
            summary['pii_by_type'][pii_type] += 1

        return summary