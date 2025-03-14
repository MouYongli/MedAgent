from abc import ABC
from typing import TYPE_CHECKING, Dict, Any
from openai import OpenAI, OpenAIError
from app.models.workflow import Generator

if TYPE_CHECKING:
    from app.models.chat import Chat

class DeepSeekGenerator(Generator, ABC):
    """
    Concrete implementation of BaseGenerator for DeepSeek's models.
    """

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.model_name = "deepseek-chat"
        self.parameters = {}
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """Returns required parameters for DeepSeekGenerator."""
        return {
            "api_key": {"type": "str", "description": "API key for authenticating with DeepSeek"},
        }

    def generate_response(self, conversation_context: "Chat") -> str:
        """Generates a response using the DeepSeek model."""
        messages = [
            {"role": "user" if msg.messageType == "question" else "assistant", "content": msg.content}
            for msg in conversation_context.messages
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            return f"Error from DeepSeek: {str(e)}"

    def get_model_info(self) -> dict:
        return {
            "model_name": self.model_name,
            "provider": "DeepSeek"
        }
