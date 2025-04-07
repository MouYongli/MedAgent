from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.system.WorkflowSystem import WorkflowSystem


class MessageType(Enum):
    QUESTION = "user question", # posed by user
    ANSWER = "system answer" # created by system

class ConversationMessage:
    def __init__(self, message_type: MessageType, content: str):
        self.messageType: MessageType = message_type
        self.content = content
        self.timestamp = datetime.now(timezone.utc)

    def __repr__(self):
        return f"[{self.timestamp}] {self.messageType.value}: {self.content}"

class Chat:
    def __init__(self, system: "WorkflowSystem", user: str = "no user"):
        self.id = str(uuid4())
        self.messages = []
        self.user = user
        self.system: WorkflowSystem = system

    def add_message(self, message_type: MessageType, content: str):
        message = ConversationMessage(message_type, content)
        self.messages.append(message)

    def pose_question(self, question: str) -> str:
        # TODO: maybe adjust return value to something else later (not only string, but also retrieved context etc.)
        self.add_message(MessageType.QUESTION, question)
        return self.generate_response()

    def generate_response(self) -> str:
        response = self.system.generate_response(self)
        self.add_message(MessageType.ANSWER, response)
        return response
