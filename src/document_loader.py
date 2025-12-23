import os
from pathlib import Path
from typing import List, Dict
import pypdf
from docx import Document
import markdown

class DocumentLoader:
    """Load documents from various file formats."""

    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.supported_formats = {'.pdf', '.txt', '.md', '.docx', '.py', '.js', '.java'}

    def load_pdf(self, filepath: Path) -> str:
        """Extract text from PDF."""
        text = []
        with open(filepath, 'rb') as file:
            pdf = pypdf.PdfReader(file)
            for page in pdf.pages:
                text.append(page.extract_text())
        return "\n".join(text)

    def load_docx(self, filepath: Path) -> str:
        """Extract text from DOCX."""
        doc = Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def load_text(self, filepath: Path) -> str:
        """Load plain text files."""
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    def load_document(self, filepath: Path) -> Dict:
        """Load a single document with metadata."""
        suffix = filepath.suffix.lower()

        if suffix == '.pdf':
            content = self.load_pdf(filepath)
        elif suffix == '.docx':
            content = self.load_docx(filepath)
        elif suffix in {'.txt', '.md', '.py', '.js', '.java'}:
            content = self.load_text(filepath)
        else:
            raise ValueError(f"Unsupported format: {suffix}")

        return {
            'content': content,
            'metadata': {
                'filename': filepath.name,
                'filepath': str(filepath),
                'file_type': suffix,
                'size_bytes': filepath.stat().st_size
            }
        }

    def load_all(self) -> List[Dict]:
        """Load all supported documents from data directory."""
        documents = []

        for filepath in self.data_dir.rglob('*'):
            if filepath.is_file() and filepath.suffix.lower() in self.supported_formats:
                try:
                    doc = self.load_document(filepath)
                    documents.append(doc)
                    print(f"Loaded: {filepath.name}")
                except Exception as e:
                    print(f"Error loading {filepath.name}: {e}")

        return documents