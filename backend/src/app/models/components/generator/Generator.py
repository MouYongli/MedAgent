from abc import abstractmethod
from typing import TYPE_CHECKING, Dict, Any, Type, Optional
from app.models.components.AbstractComponent import AbstractComponent

if TYPE_CHECKING:
    from app.models.chat import Chat


class Generator(AbstractComponent, variant_name="generator"):
    variants: Dict[str, Type['Generator']] = {}
    default_parameters: Dict[str, Any] = {
        "max_tokens": 256,
        "temperature": 0.7
    }

    def __init__(self, name: str, inputs: Dict[str, Any], outputs: Dict[str, Any], parameters: Dict[str, Any], variant: str = None):
        super().__init__(name, inputs, outputs, parameters, variant)

    def __init_subclass__(cls, variant_name: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if variant_name:
            Generator.variants[variant_name] = cls

    @classmethod
    @abstractmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        pass

    @abstractmethod
    def generate_response(self, conversation: "Chat") -> str:
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        pass

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        chat: "Chat" = data["chat"]
        return {"response": self.generate_response(chat)}
