from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.schemas.generate_request import GenerateRequest
from app.schemas.generate_response import GenerateResponse
from app.services.generator_service import generate_text_service, call_ollama_api_stream

router = APIRouter()


@router.post("/", response_model=GenerateResponse)
def generate_text(request: GenerateRequest):
    answer = generate_text_service(request.query)
    return GenerateResponse(result=answer)


@router.post("/stream")
def stream_generate_text(request: GenerateRequest):
    def event_stream():
        for chunk in call_ollama_api_stream(request.query):
            yield chunk

    return StreamingResponse(event_stream(), media_type="application/json")
