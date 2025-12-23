from typing import List, Dict
import re

class SemanticChunker:
    """Advanced chunking with semantic awareness."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_by_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitter
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk_by_semantic_units(self, text: str, metadata: Dict) -> List[Dict]:
        """Create chunks respecting semantic boundaries."""
        sentences = self.split_by_sentences(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            # If adding this sentence exceeds chunk_size, finalize current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        **metadata,
                        'chunk_index': len(chunks),
                        'chunk_length': len(chunk_text)
                    }
                })

                # Create overlap by keeping sentences that fit within chunk_overlap
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    s_len = len(s)
                    if overlap_length + s_len <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += s_len
                    else:
                        break

                # Start new chunk with overlap + current sentence
                current_chunk = overlap_sentences + [sentence]
                current_length = sum(len(s) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        # Add final chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    **metadata,
                    'chunk_index': len(chunks),
                    'chunk_length': len(chunk_text)
                }
            })

        return chunks

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Chunk all documents."""
        all_chunks = []

        for doc in documents:
            doc_chunks = self.chunk_by_semantic_units(
                doc['content'],
                doc['metadata']
            )
            all_chunks.extend(doc_chunks)

        return all_chunks