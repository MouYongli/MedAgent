import os
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse
import weaviate
from weaviate.classes.config import Configure, Property, DataType
import logging

router = APIRouter()

weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8081")
parsed_weaviate_url = urlparse(weaviate_url)
weaviate_client = weaviate.connect_to_custom(
    http_host=parsed_weaviate_url.hostname,
    http_port=parsed_weaviate_url.port,
    http_secure=parsed_weaviate_url.scheme == "https",
    grpc_host=parsed_weaviate_url.hostname,
    grpc_port=50051,
    grpc_secure=parsed_weaviate_url.scheme == "https",
)
weaviate_client.connect()

AVAILABLE_VECTORIZERS = ["none", "text2vec-transformers"]
def get_vectorizer_config(vectorizer: str, source_properties: List[str]):
    if vectorizer == "none":
        return Configure.Vectorizer.none()
    elif vectorizer == "text2vec-transformers":
        return [Configure.NamedVectors.text2vec_transformers(name='default', source_properties=source_properties)]
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported vectorizer '{vectorizer}'. Supported: {AVAILABLE_VECTORIZERS}")


def validate_class_exists(class_name: str):
    if not weaviate_client.collections.exists(class_name):
        raise HTTPException(
            status_code=404,
            detail=f"Weaviate class '{class_name}' does not exist."
        )

logger = logging.getLogger(__name__)

# Pydantic models for API
class SchemaProperty(BaseModel):
    name: str
    data_type: str  # single string like "text", "int", "number", "bool", "date", or "uuid"
    description: Optional[str] = None
    moduleConfig: Optional[dict] = None

class InitRequest(BaseModel):
    class_name: str
    description: Optional[str] = "A Weaviate class"
    vectorizer: Optional[str] = None
    vectorizer_properties: Optional[List[str]] = None
    properties: List[SchemaProperty]
    moduleConfig: Optional[dict] = None

class ChunkInsert(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None
    vector: Optional[List[float]] = None # only used if vectorizer is none
    class_name: str

class ChunkBatchInsert(BaseModel):
    class_name: str
    entries: List[ChunkInsert]

class ChunkQuery(BaseModel):
    query: str
    top_k: int = 5
    class_name: str
    vector: Optional[List[float]] = None # only used if vectorizer is none

# --- ROUTES ---
@router.get("/retriever/vectorizers")
def list_vectorizers():
    return {"available_vectorizers": AVAILABLE_VECTORIZERS}

@router.delete("/retriever/delete/{class_name}")
def delete_weaviate_collection(class_name):
    if not weaviate_client.collections.exists(class_name):
        raise HTTPException(status_code=404, detail=f"Class '{class_name}' does not exist.")

    weaviate_client.collections.delete(class_name)
    logger.info(f"Deleted Weaviate class: {class_name}")
    return {"status": "deleted", "class": class_name}

@router.post("/retriever/init")
def init_weaviate_collection(req: InitRequest):
    if weaviate_client.collections.exists(req.class_name):
        logger.error(f"Weaviate class {req.class_name} already existed in vector database")
        raise HTTPException(status_code=400, detail=f"Class '{req.class_name}' already exists in Weaviate.")

    # Convert SchemaProperty Pydantic model to dict (as expected in 4.13.2)
    properties = [
        Property(name=p.name, data_type=DataType(p.data_type), description=p.description)
        for p in req.properties
    ]

    # Set vectorizer config to "none" as a plain string
    vectorizer = req.vectorizer or "none"
    def validate_vectorizer_properties(vec_props, vec, props):
        if vec_props:
            property_map = {p.name: p.data_type for p in props}
            for prop in vec_props:
                if prop not in property_map:
                    raise HTTPException(status_code=400, detail=f"Property '{prop}' is not defined in the schema.")
                if property_map[prop] != "text":
                    raise HTTPException(status_code=400, detail=f"Property '{prop}' is not of type 'text'.")
        else:
            if vec != "none":
                raise HTTPException(status_code=400, detail=f"To configure a vectorizer ({vec}), a list of vectorizer properties needs to be provided specifying what to use as index")
    validate_vectorizer_properties(req.vectorizer_properties, vectorizer, req.properties)
    source_props = req.vectorizer_properties or []
    vectorizer_config = get_vectorizer_config(vectorizer, source_props)

    weaviate_client.collections.create(
        name=req.class_name,
        description=req.description,
        vectorizer_config=vectorizer_config,
        properties=properties
    )

    logger.info(f"Created new Weaviate class schema: {req.class_name}")
    return {"status": "initialized", "class": req.class_name}


@router.post("/retriever/insert")
def insert_chunk(chunk: ChunkInsert):
    logger.info(f"Insert request received for class: {chunk.class_name}")
    logger.debug(f"Chunk content: {chunk.text[:100]}...")
    logger.debug(f"Metadata: {chunk.metadata}")
    logger.debug(f"Vector present: {'yes' if chunk.vector else 'no'}")

    validate_class_exists(chunk.class_name)

    collection = weaviate_client.collections.get(chunk.class_name)

    def is_auto_vectorized(collection) -> bool:
        vector_config = collection.config.get().vector_config
        if not vector_config:
            return False
        else:
            return True

    auto_vectorized = is_auto_vectorized(collection)

    try:
        data_obj = {
            "text": chunk.text,
            **(chunk.metadata or {})
        }

        if not auto_vectorized:
            if chunk.vector is None:
                logger.error("Manual vector required but not provided.")
                raise HTTPException(status_code=400, detail="Class requires manual vector, but none was provided.")
            collection.data.insert(properties=data_obj, vector=chunk.vector)
        else:
            if chunk.vector is not None:
                logger.warning(f"Ignoring provided vector for class '{chunk.class_name}' with built-in vectorizer")
            collection.data.insert(properties=data_obj)

        logger.info(f"Successfully inserted into class '{chunk.class_name}'")
        return {"status": "inserted", "class": chunk.class_name}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to insert chunk into class '{chunk.class_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to insert: {str(e)}")

@router.post("/retriever/insertBatch")
def insert_chunk_batch(batch: ChunkBatchInsert):
    logger.info(f"Batch insert request received for class: {batch.class_name}")
    validate_class_exists(batch.class_name)

    collection = weaviate_client.collections.get(batch.class_name)

    def is_auto_vectorized(collection) -> bool:
        vector_config = collection.config.get().vector_config
        return bool(vector_config)

    auto_vectorized = is_auto_vectorized(collection)
    failed = []
    total = len(batch.entries)

    with collection.batch.fixed_size(batch_size=25, concurrent_requests=4)  as batcher:
        for entry in batch.entries:
            data_obj = {
                "text": entry.text,
                **(entry.metadata or {})
            }

            try:
                if not auto_vectorized:
                    if entry.vector is None:
                        logger.warning("Manual vector required but not provided. Skipping entry.")
                        failed.append(entry.metadata["chunk_index"])
                        continue
                    batcher.add_object(
                        properties=data_obj,
                        uuid=str(uuid4()),
                        vector=entry.vector
                    )
                else:
                    if entry.vector is not None:
                        logger.warning(f"Ignoring vector for auto-vectorized class '{batch.class_name}'")
                    batcher.add_object(
                        properties=data_obj,
                        uuid=str(uuid4())
                    )
            except Exception as e:
                logger.exception(f"Failed to queue entry in batch: {e}")
                failed.append(entry.metadata["chunk_index"])

    # Handle any post-batch failures
    if collection.batch.failed_objects:
        logger.error(f"Failed batch objects: {len(collection.batch.failed_objects)}")
        for obj in collection.batch.failed_objects:
            chunk_id = obj.get("properties", {}).get("chunk_index", "<unknown>")
            failed.append(chunk_id)

    logger.info(f"Batch insert complete: {total - len(failed)} succeeded, {len(failed)} failed.")
    return {
        "class": batch.class_name,
        "status": "completed",
        "success": total - len(failed),
        "failed": failed
    }


@router.post("/retriever/search")
def search_chunk(query: ChunkQuery):
    validate_class_exists(query.class_name)

    collection = weaviate_client.collections.get(query.class_name)
    vectorizer = collection.config.vectorizer_config.name

    if vectorizer == "none":
        if query.vector is None:
            raise HTTPException(status_code=400, detail=f"Class '{query.class_name}' uses manual vectorization — you must provide a vector.")
        query_result = collection.query.near_vector(query.vector, limit=query.top_k).fetch_objects()
    else:
        if query.vector is not None:
            logger.warning(
                f"Ignoring provided vector for class '{query.class_name}' with built-in vectorizer '{vectorizer}'")
        query_result = collection.query.near_text(query.query, limit=query.top_k).fetch_objects()

    return {"results": [obj.properties for obj in query_result.objects]}

