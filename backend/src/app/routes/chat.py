from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.chat import Chat, MessageType
from app.models.generators.SimpleGenerator import SimpleGenerator

router = APIRouter()

conversations: Dict[str, Chat] = {}

class InitResponse(BaseModel):
    conversation_id: str
    message: str

class MessageRequest(BaseModel):
    conversation_id: str
    message: str

class MessageResponse(BaseModel):
    conversation_id: str
    message: str

@router.post("/init", response_model=InitResponse)
async def init_conversation():
    conversation = Chat(generator=SimpleGenerator())
    message = f'Welcome, this is chat {conversation.id}'
    conversation.add_message(MessageType.ANSWER, message)
    conversations[conversation.id] = conversation
    return InitResponse(conversation_id=conversation.id, message=message)

@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    conversation = conversations.get(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    response = conversation.pose_question(request.message)
    return MessageResponse(conversation_id=conversation.id, message=response)
