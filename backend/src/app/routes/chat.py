from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.chat import Conversation

router = APIRouter()

conversations = {}

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
    conversation = Conversation()
    conversation.add_message('System', 'Welcome')
    conversations[conversation.id] = conversation
    return InitResponse(conversation_id=conversation.id, message='Welcome')

@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    conversation = conversations.get(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation.add_message('User', request.message)
    response = conversation.get_response()
    conversation.add_message('System', response)
    return MessageResponse(conversation_id=conversation.id, message=response)
