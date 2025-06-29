from app.schemas.chat_response import ChatResponse
from fastapi import APIRouter, HTTPException
from app.schemas.chat_message import ChatMessage
from typing import List
from app.services.chat_service import (
    get_chat_history_service,
    send_message_service,
    send_message_stream_service,
    send_message_stream_service_graph,
    send_message_stream_service_vector,
)
from fastapi.responses import StreamingResponse
import json

router = APIRouter()


@router.get("/history", response_model=List[ChatMessage])
def get_chat_history():
    return get_chat_history_service()


@router.post("/send", response_model=ChatResponse)
def send_message(request: ChatMessage):
    response = send_message_service(request.content)

    return ChatResponse(
        query=request.content, chunks=response["chunks"], result=response["result"]
    )


@router.post("/send/stream")
def send_message_stream(request: ChatMessage):
    def event_stream():
        for chunk in send_message_stream_service(request.content):
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(event_stream(), media_type="application/json")


@router.post("/send/stream/vector")
def send_message_vector_stream(request: ChatMessage):
    def event_stream():
        for chunk in send_message_stream_service_vector(request.content):
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(event_stream(), media_type="application/json")


@router.post("/send/stream/graph")
def send_message_graph_stream(request: ChatMessage):
    def event_stream():
        for chunk in send_message_stream_service_graph(request.content):
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(event_stream(), media_type="application/json")
