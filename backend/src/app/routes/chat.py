from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.chat import Chat, MessageType
from app.models.generators.OpenAIGenerator import OpenAIGenerator
from app.models.generators.SimpleGenerator import SimpleGenerator

router = APIRouter()

conversations: Dict[str, Chat] = {}

class InitRequest(BaseModel):
    generator_name: str  # Name of the generator to use
    parameters: Dict[str, Any]  # Parameters required for the generator

class InitResponse(BaseModel):
    conversation_id: str
    message: str

class MessageRequest(BaseModel):
    conversation_id: str
    message: str

class MessageResponse(BaseModel):
    conversation_id: str
    message: str

GENERATORS = {
    "simple": SimpleGenerator,
    "openai": OpenAIGenerator
}

@router.get("/generators") # Maybe move to workflow??
async def list_generators() -> Dict[str, Dict[str, Any]]:
    """Returns all available generators and their required parameters."""
    return {name: gen.get_init_parameters() for name, gen in GENERATORS.items()}

@router.post("/init", response_model=InitResponse)
async def init_conversation(request: InitRequest):
    if request.generator_name not in GENERATORS:
        raise HTTPException(status_code=400, detail="Invalid generator name")

    generator_class = GENERATORS[request.generator_name]
    expected_params = generator_class.get_init_parameters()
    for param, details in expected_params.items():
        if param not in request.parameters:
            raise HTTPException(status_code=400, detail=f"Missing required parameter: {param}")

        expected_type = eval(details["type"])  # Convert type string to actual Python type
        if not isinstance(request.parameters[param], expected_type):
            raise HTTPException(
                status_code=400,
                detail=f"Incorrect type for {param}: expected {details['type']}, got {type(request.parameters[param])}"
            )
    generator = generator_class(**request.parameters)

    conversation = Chat(generator=generator)
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
