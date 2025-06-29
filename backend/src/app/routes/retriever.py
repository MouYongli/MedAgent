from app.services.graph_retriever_service import retrieve_chunks_graph_db
from fastapi import APIRouter, HTTPException
from app.schemas.retriever_request import RetrieverRequest
from app.schemas.retriever_response import RetrieverResponse
from app.services.generator_service import generate_text_service
from app.services.vector_retriever_service import retrieve_chunks_vector_db

router = APIRouter()


@router.post("/vector", response_model=RetrieverResponse)
def retrieve_from_vector_db(request: RetrieverRequest):
    retrieved_chunks = retrieve_chunks_vector_db(request.query)

    return RetrieverResponse(query=request.query, chunks=retrieved_chunks)


@router.post("/graph", response_model=RetrieverResponse)
def retrieve_from_graph_db(request: RetrieverRequest):
    retrieved_chunks = retrieve_chunks_graph_db(request.query)

    return RetrieverResponse(query=request.query, chunks=retrieved_chunks)
