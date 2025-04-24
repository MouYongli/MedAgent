from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Any, Dict
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.system.WorkflowSystem import WorkflowSystem


class MessageType(Enum):
    QUESTION = "user question",  # posed by user
    ANSWER = "system answer"  # created by a system


class ChatResponse:
    """
    Encapsulates the workflow response and metadata.
    """

    def __init__(self, response: str, retrieval: List[Dict[str, Any]], execution_time: float):
        self.response = response
        self.retrieval = retrieval
        self.execution_time = execution_time

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response object to a dictionary for API serialization.
        """
        return {
            "response": self.response,
            "retrieval": self.retrieval,
            "execution_time": self.execution_time,
        }

    def __str__(self) -> str:
        """
        String representation of the response object.
        """
        return f"WorkflowResponse(response={self.response}, retrieval={self.retrieval}, execution_time={self.execution_time:.2f}s)"


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

    def pose_question(self, question: str) -> ChatResponse:
        # TODO: maybe adjust return value to something else later (not only string, but also retrieved context etc.)
        self.add_message(MessageType.QUESTION, question)
        return self.generate_response()

    def generate_response(self) -> ChatResponse:
        workflow_response = self.system.generate_response(self)
        self.add_message(MessageType.ANSWER, workflow_response.response)
        return workflow_response
