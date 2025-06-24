from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class SemanticChunk:
    chunk_id: str
    page_content: str
    title: str
    summary: str
    chunk_index: int  # could remove
    page_number: str
    book_name: str
    embedding: list[float] = None
