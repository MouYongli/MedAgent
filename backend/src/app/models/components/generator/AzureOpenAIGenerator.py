from openai import AzureOpenAI
import os
from typing import Dict, Any, TYPE_CHECKING

from openai.types.chat import ChatCompletionMessageParam

from app.models.components.generator.Generator import Generator

if TYPE_CHECKING:
    from app.models.chat import Chat

class AzureOpenAIGenerator(Generator, variant_name="azure_openai"):
    default_parameters: Dict[str, Any] = {
        "api_key": os.getenv("AZURE_OPENAI_API_KEY", ""),
        "api_base": os.getenv("AZURE_OPENAI_API_BASE", ""),
        "api_type": os.getenv("AZURE_OPENAI_API_TYPE", "azure"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-18"),
        "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        "temperature": float(os.getenv("AZURE_OPENAI_TEMPERATURE", 0.7)),
        "max_tokens": int(os.getenv("AZURE_OPENAI_MAX_TOKENS", 256)),
    }

    def __init__(self, name: str, inputs: Dict[str, Any], outputs: Dict[str, Any], parameters: Dict[str, Any], variant: str = None):
        super().__init__(name, inputs, outputs, parameters, variant)
        self.client = AzureOpenAI(
            api_key=parameters.get("api_key", ""),
            api_version=parameters.get("api_version", ""),
            azure_endpoint=parameters.get("api_base", "")
        )

    def generate_response(self, conversation: "Chat") -> str:
        messages = []
        for msg in conversation.messages:
            if msg.messageType.name == "QUESTION":
                role = "user"
            elif msg.messageType.name == "ANSWER":
                role = "assistant"
            else:
                continue
            messages.append({"role": role, "content": msg.content})

        response = self.client.chat.completions.create(
            model=self.parameters["deployment_name"],
            messages=messages,
            temperature=self.parameters["temperature"],
            max_tokens=self.parameters["max_tokens"]
        )
        return response.choices[0].message.content

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "Azure OpenAI",
            "deployment": self.parameters["deployment_name"],
            "version": self.parameters["api_version"]
        }

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "api_key": {"type": "string", "description": "Azure OpenAI API key"},
            "api_base": {"type": "string", "description": "Azure OpenAI API base URL"},
            "api_type": {"type": "string", "description": "API type (usually 'azure')"},
            "api_version": {"type": "string", "description": "API version used by Azure OpenAI"},
            "deployment_name": {"type": "string", "description": "Azure OpenAI deployment name"},
            "temperature": {"type": "float", "description": "Controls randomness in output (0.0 - 1.0)"},
            "max_tokens": {"type": "int", "description": "Maximum number of tokens to generate"}
        }
