from abc import ABC
from typing import TYPE_CHECKING

# import openai

from app.models.workflow import Generator

if TYPE_CHECKING:
    from app.models.chat import Chat

class OpenAIGenerator(Generator, ABC):
    """
    Concrete implementation of BaseGenerator for OpenAI's GPT models.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.parameters = {}
        # openai.api_key = self.api_key

    def generate_response(self, conversation_context: "Chat") -> str:
        """Generates a simple numbered response."""
        pass


    def get_model_info(self) -> dict:
        return {
            "model_name": self.model_name,
            "provider": "OpenAI"
        }
