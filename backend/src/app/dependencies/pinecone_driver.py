from pinecone import Pinecone
from app.config import config

# Singleton instance for Pinecone index
_index = None


def get_pinecone_index():
    global _index
    if _index is None:
        pc = Pinecone(config["Database"]["PINECONE_API_KEY"])
        _index = pc.Index(config["Database"]["PINECONE_INDEX_NAME"])
    return _index
