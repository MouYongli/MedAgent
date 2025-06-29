import os

os.environ["TORCH_LOAD_WEIGHTS_ONLY"] = "False"
from typing import List, Dict
from app.dependencies.graph_retriever import get_graph_retriever


def retrieve_chunks_graph_db(query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve top_k most similar vectors from Pinecone index.
    """
    graph_retriever = get_graph_retriever(top_k)
    retrieved_chunks = graph_retriever.retrieve_chunks(query)

    return retrieved_chunks
