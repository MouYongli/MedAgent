from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Simple counter variables to track interactions
interaction_counters = {"input_count": 0, "output_count": 0}

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    input_count: int
    output_count: int
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_system(request: ChatRequest):
    interaction_counters["input_count"] += 1
    interaction_counters["output_count"] += 1  # For now, we assume one reply per message

    response_message = f"This is message #{interaction_counters['input_count']}"

    return ChatResponse(
        input_count=interaction_counters["input_count"],
        output_count=interaction_counters["output_count"],
        reply=response_message
    )
