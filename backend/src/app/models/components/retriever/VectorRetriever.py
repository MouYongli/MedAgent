import asyncio
import logging
from typing import Dict, Any

import httpx
import nest_asyncio

from app.models.components.retriever.Retriever import Retriever
from app.utils.helper import render_template

logger = logging.getLogger(__name__)


class VectorRetriever(Retriever, variant_name="vector_weaviate"):
    DEFAULT_ENDPOINT = "http://host.docker.internal:5000/api/knowledge/vector/retriever/search"

    async def async_retrieve(self, query: str, top_k: int, data: Dict[str, Any]) -> list:
        class_name = self.parameters.get("class_name")
        endpoint = self.parameters.get("endpoint", self.DEFAULT_ENDPOINT)
        vector = self.parameters.get("vector", None)
        vector = render_template(vector, data) if vector else None

        logger.info(
            f"[VectorRetriever] Endpoint: {endpoint}, Class: {class_name}, Query: {query}, TopK: {top_k}, Using vector: {bool(vector)}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, json={
                    "query": query,
                    "top_k": top_k,
                    "class_name": class_name,
                    "vector": vector,
                }, timeout=30.0)

            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            logger.exception("[VectorRetriever] Retrieval failed")
            raise RuntimeError(f"VectorRetriever failed to query Weaviate: {e}")

    def retrieve(self, query: str, top_k: int, data: Dict[str, Any]) -> list:
        """
        Synchronous function that wraps async_retrieve.
        This ensures proper handling within a running event loop using nest_asyncio.
        """
        try:
            loop = asyncio.get_event_loop()
            nest_asyncio.apply(loop)  # Allow nested event loop usage
            if loop.is_running():
                # Use asyncio.ensure_future to schedule the coroutine's execution
                future = asyncio.ensure_future(self.async_retrieve(query=query, top_k=top_k, data=data))
                return loop.run_until_complete(future)
            else:
                return loop.run_until_complete(self.async_retrieve(query=query, top_k=top_k, data=data))
        except Exception as e:
            logger.error(f"[VectorRetriever] Failed to execute retrieve: {e}", exc_info=True)
            raise RuntimeError(f"Retriever encountered an issue: {e}")
