from abc import ABC
from typing import TYPE_CHECKING, Dict, Any

from openai import OpenAI, OpenAIError

from app.models.workflow import Generator

if TYPE_CHECKING:
    from app.models.chat import Chat

class OpenAIGenerator(Generator, ABC):
    """
    Concrete implementation of BaseGenerator for OpenAI's GPT models.
    """

    def __init__(self, api_key: str, model_name: str):
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.parameters = {}
        self.client = OpenAI(api_key=self.api_key)

        # TEST
        response = self.client.responses.create(
            model="gpt-4o",
            instructions="Respond very briefly.",
            input="Answer with hello world. Thanks!!"
        )
        print(response.output_text)

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """Returns required parameters for OpenAIGenerator."""
        return {
            "api_key": {"type": "str", "description": "API key for authenticating with OpenAI"},
            "model_name": {"type": "str", "description": "OpenAI model to use, e.g., 'gpt-3.5-turbo'"},
        }

    def generate_response(self, conversation_context: "Chat") -> str:
        """Generates a simple numbered response."""
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
            return f"Error from OpenAI: {str(e)}"

    def get_model_info(self) -> dict:
        return {
            "model_name": self.model_name,
            "provider": "OpenAI"
        }
