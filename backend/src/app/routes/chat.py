
from app.schemas.chat_message import ChatMessage
from app.schemas.chat_response import ChatResponse
from app.services.chat_service import send_message
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.services.generator_service import generate_text_service, call_ollama_api_stream

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def respond_to_user(request: ChatMessage):
    response = send_message(request.query)
    return ChatResponse(
        query=request.query, chunks=response["chunks"], result=response["result"]
    )
