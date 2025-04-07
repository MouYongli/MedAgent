from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from app.models.chat import Chat, MessageType
from app.routes.workflow import get_workflow

router = APIRouter()
chat_sessions: Dict[str, Chat] = {}

# Pydantic models
class InitChatRequest(BaseModel):
    workflow_id: str

class InitChatResponse(BaseModel):
    chat_id: str
    workflow_id: str
    message: str

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    chat_id: str
    response: str

@router.post("/init", response_model=InitChatResponse)
async def init_chat(request: InitChatRequest):
    workflow = get_workflow(request.workflow_id)
    chat = Chat(system=workflow)
    chat_sessions[chat.id] = chat

    welcome = f"New chat session {chat.id} created for workflow {request.workflow_id}"
    chat.add_message(MessageType.ANSWER, welcome)

    return InitChatResponse(
        chat_id=chat.id,
        workflow_id=request.workflow_id,
        message=welcome
    )

@router.post("/{chat_id}/ask", response_model=AskResponse)
async def ask_chat(chat_id: str, request: AskRequest):
    chat = chat_sessions.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat ID not found")

    response = chat.pose_question(request.question)
    return AskResponse(chat_id=chat.id, response=response)

@router.get("/list")
async def list_chats() -> Dict[str, str]:
    return {cid: f"Chat session" for cid in chat_sessions}
