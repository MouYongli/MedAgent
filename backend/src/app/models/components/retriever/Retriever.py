import logging
from abc import abstractmethod
from typing import Dict, Any, Type, Optional
from app.models.components.AbstractComponent import AbstractComponent

from app.utils.helper import resolve_template

logger = logging.getLogger(__name__)

class Retriever(AbstractComponent, variant_name="retriever"):
    variants: Dict[str, Type['Retriever']] = {}

    def __init__(self, id: str, name: str, parameters: Dict[str, Any], variant: str = None):
        super().__init__(id, name, parameters, variant)

    def __init_subclass__(cls, variant_name: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if variant_name:
            Retriever.variants[variant_name] = cls

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "query": {
                "type": "string",
                "description": "Term based on which the 'most relevant' entries are extracted (will be resolved with the variables specified)"
            },
            "top_k": {
                "type": "int",
                "description": "Number of top results to retrieve (defaults to 5)"
            }
        }

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "retriever.results": {
                "type": "list",
                "description": "List of retrieved objects based on semantic similarity"
            }
        }

    @abstractmethod
    def retrieve(self, query: str, top_k: int, data: Dict[str, Any]) -> list:
        pass

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query_template = self.parameters["query"]
            query = resolve_template(query_template, data)
            top_k = int(self.parameters.get("top_k", 5))

            logger.info(f"[Retriever] Query: {query} | TopK: {top_k}")
            results = self.retrieve(query=query, top_k=top_k, data=data)
            data[f"{self.id}.results"] = results
            return data

        except Exception as e:
            logger.exception("[Retriever] Failed to retrieve:")
            raise RuntimeError(f"Retriever execution failed: {e}")
