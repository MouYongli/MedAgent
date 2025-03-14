from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from app.models.workflow import Generator


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
    def __init__(self, generator: Generator, user: str = "no user"):
        self.id = str(uuid4())
        self.messages = []
        self.user = user # userID -> string?
        self.system: Generator = generator # Maybe later systemID? Then call this via another API call?

    def add_message(self, message_type: MessageType, content: str):
        message = ConversationMessage(message_type, content)
        self.messages.append(message)

    def pose_question(self, question: str) -> str:
        self.add_message(MessageType.QUESTION, question)
        return self.generate_response()

    def generate_response(self) -> str:
        response = self.system.generate_response(self)
        self.add_message(MessageType.ANSWER, response)
        return response
