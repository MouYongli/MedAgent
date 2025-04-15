import re
from abc import abstractmethod
from typing import Dict, Any, Type, Optional
from app.models.components.AbstractComponent import AbstractComponent


class Generator(AbstractComponent, variant_name="generator"):
    variants: Dict[str, Type['Generator']] = {}
    default_parameters: Dict[str, Any] = {
        "prompt": "{start.current_user_input}"
    }

    def __init__(self, id: str, name: str, parameters: Dict[str, Any], variant: str = None):
        super().__init__(id, name, parameters, variant)

    def __init_subclass__(cls, variant_name: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if variant_name:
            Generator.variants[variant_name] = cls

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "prompt": {
                "type": "string",
                "description": "Prompt template with placeholders resolved before generation"
            }
        }

    @classmethod
    def get_input_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "start.chat.current_user_input": {
                "type": "string",
                "description": "Latest user message content from the chat context under the 'start' namespace (or whatever the name of the respective component is)"
            }
        }

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "generator.response": {
                "type": "string",
                "description": "Generated response string based on the resolved prompt under the 'generator' namespace (or whatever the name of the component is)"
            }
        }

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        pass

    @staticmethod
    def resolve_prompt(template: str, context: Dict[str, Any]) -> str:
        def replacer(match):
            key_path = match.group(1)
            try:
                return str(AbstractComponent.resolve_data_path(key_path, context))
            except Exception as e:
                return f"<Error resolving {key_path}: {e}>"

        return re.sub(r"\{(.*?)\}", replacer, template)

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt_template = self.parameters.get("prompt", self.default_parameters.get("prompt"))
        prompt = self.resolve_prompt(prompt_template, data)
        data[self.id] = {"response": self.generate_response(prompt)}
        return data
