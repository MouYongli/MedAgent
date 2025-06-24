from app.schemas.chunk import Chunk
from sentence_transformers import SentenceTransformer
import numpy as np
from app.dependencies.pinecone_driver import get_pinecone_index
from app.dependencies.para_chunks import load_para_chunks


class VectorRetriever:
    def __init__(self, K, driver):
        self.top_K = K
        self.driver = driver
        self.model = SentenceTransformer(
            "SeanLee97/mxbai-embed-large-v1-nli-matryoshka",
            device="cpu",
            trust_remote_code=True,
        )

    def get_query_vector(self, query):
        return self.model.encode(query).tolist()

    def retrieve_chunk_ids(self, query):
        embedding = self.get_query_vector(query)

        matches = self.driver.query(
            vector=embedding, top_k=self.top_K, include_metadata=True
        )
        # title most similar to query
        retrieved_data = matches["matches"]

        top_K_chunks = np.array([int(obj["id"]) for obj in retrieved_data])
        return top_K_chunks

    def retrieve_chunks(self, query):
        top_K_chunks = self.retrieve_chunk_ids(query)
        para_chunks = load_para_chunks()
        chunks = []
        for id in top_K_chunks:
            chunks.append(
                Chunk(
                    page_content=para_chunks[id].page_content,
                    book_name=para_chunks[id].book_name,
                    page_number=para_chunks[id].page_number,
                    id=id,
                )
            )
        # return "\n\n".join(chunks)
        return chunks


_vector_retriever = None


def get_vector_retriever(top_k: int = 5):
    global _vector_retriever
    from app.dependencies.vector_retriever import (
        VectorRetriever,
    )  # Avoid circular import

    if _vector_retriever is None or _vector_retriever.top_K != top_k:
        _vector_retriever = VectorRetriever(K=top_k, driver=get_pinecone_index())
    return _vector_retriever
