from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from app.models.chat import Chat

class Generator(ABC):
    """Abstract base class for generators."""

    def __init__(self):
        """Setup whatever is needed for the generator."""
        pass  # Can be used for API keys, model setup, etc.

    @classmethod
    @abstractmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """
        Returns required parameters for initializing the generator.

        :return: A dictionary where keys are parameter names and values are dictionaries
                 containing 'type' and 'description' fields.
        """
        pass

    @abstractmethod
    def generate_response(self, conversation: "Chat") -> str:
        """Generates a response given the conversation context."""
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Retrieve information about the model, such as its name and version.

        :return: A dictionary containing model information.
        """
        pass
