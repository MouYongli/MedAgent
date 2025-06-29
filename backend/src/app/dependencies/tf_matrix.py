import pickle
import os


_tf_matrix = None


def load_tf_matrix():
    """
    Loads the para_chunks list from the pickle file as a singleton.
    Returns:
        List[SemanticChunk]: List of SemanticChunk objects.
    """
    global _tf_matrix
    if _tf_matrix is None:
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        file_path = os.path.join(base_dir, "src/app/data", "tf_matrix.pkl")
        with open(file_path, "rb") as f:
            _tf_matrix = pickle.load(f)
    return _tf_matrix


# Usage example:
# para_chunks = load_para_chunks()
