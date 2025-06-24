import os

os.environ["TORCH_LOAD_WEIGHTS_ONLY"] = "False"
from typing import List, Dict
from app.dependencies.vector_retriever import get_vector_retriever


def retrieve_chunks_vector_db(query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve top_k most similar vectors from Pinecone index.
    """
    vector_retriever = get_vector_retriever(top_k)
    retrieved_chunks = vector_retriever.retrieve_chunks(query)

    return retrieved_chunks
