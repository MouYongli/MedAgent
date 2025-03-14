from abc import ABC
from typing import TYPE_CHECKING

from app.models.workflow import Generator

if TYPE_CHECKING:
    from app.models.chat import Chat


class SimpleGenerator(Generator, ABC):
    """A simple generator that returns 'This is answer #' responses."""

    def __init__(self):
        super().__init__()
        self.response_count = 0

    def generate_response(self, conversation_context: "Chat") -> str:
        """Generates a simple numbered response."""
        self.response_count += 1
        return f"This is answer #{self.response_count}"

    def get_model_info(self) -> dict:
        return {
            "deployement": "local",
            "type": "static",
            "generator": "SimpleGenerator",
        }