import pickle
import os


_para_chunks = None


def load_para_chunks():
    """
    Loads the para_chunks list from the pickle file as a singleton.
    Returns:
        List[SemanticChunk]: List of SemanticChunk objects.
    """
    global _para_chunks
    if _para_chunks is None:
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        file_path = os.path.join(
            base_dir, "src/app/data", "para_wise_semantic_chunks.pkl"
        )
        with open(file_path, "rb") as f:
            _para_chunks = pickle.load(f)
    return _para_chunks


# Usage example:
# para_chunks = load_para_chunks()
