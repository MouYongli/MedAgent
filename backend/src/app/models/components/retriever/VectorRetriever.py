import requests
from typing import Dict, Any

from app.models.components.AbstractComponent import AbstractComponent
from app.models.components.retriever.Retriever import Retriever
import logging

logger = logging.getLogger(__name__)

class VectorRetriever(Retriever, variant_name="vector_weaviate"):
    DEFAULT_ENDPOINT = "http://host.docker.internal:5000/api/knowledge/vector/retriever/search"

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        base_params = super().get_init_parameters()
        vector_weaviate_params = { # TODO: as an idea, maybe move the class name INTO the endpoint?
            "class_name": {
                "type": "string",
                "description": "Weaviate class to query"
            },
            "endpoint": {
                "type": "string",
                "description": "URL of the vector search API",
                "default": cls.DEFAULT_ENDPOINT
            },
            "vector": {
                "type": "list",
                "description": "Optional embedding vector to use for similarity search instead of auto-vectorization",
                "default": None
            }
        }
        return {**base_params, **vector_weaviate_params}

    def retrieve(self, query: str, top_k: int, data: Dict[str, Any]) -> list:
        class_name = self.parameters.get("class_name")
        endpoint = self.parameters.get("endpoint", self.DEFAULT_ENDPOINT)
        vector = self.parameters.get("vector", None)
        vector = AbstractComponent.resolve_template(vector, data) if vector else None

        logger.info(f"[VectorRetriever] Endpoint: {endpoint}, Class: {class_name}, Query: {query}, TopK: {top_k}, Using vector: {bool(vector)}")

        try:
            response = requests.post(endpoint, json={
                "query": query,
                "top_k": top_k,
                "class_name": class_name,
                "vector": vector if vector else None
            })
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            logger.exception("[VectorRetriever] Retrieval failed")
            raise RuntimeError(f"VectorRetriever failed to query Weaviate: {e}")
