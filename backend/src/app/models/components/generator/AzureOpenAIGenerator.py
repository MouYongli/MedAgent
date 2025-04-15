import logging

from openai import AzureOpenAI
import os
from typing import Dict, Any

from app.models.components.generator.Generator import Generator

logging.basicConfig(level=logging.INFO)

class AzureOpenAIGenerator(Generator, variant_name="azure_openai"):
    default_parameters: Dict[str, Any] = {
        **Generator.default_parameters,
        "api_key": os.getenv("AZURE_OPENAI_API_KEY", ""),
        "api_base": os.getenv("AZURE_OPENAI_API_BASE", ""),
        "api_type": os.getenv("AZURE_OPENAI_API_TYPE", "azure"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-18"),
        "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        "temperature": float(os.getenv("AZURE_OPENAI_TEMPERATURE", 0.7)),
        "max_tokens": int(os.getenv("AZURE_OPENAI_MAX_TOKENS", 256)),
    }

    def __init__(self, id: str, name: str, parameters: Dict[str, Any], variant: str = None):
        super().__init__(id, name, parameters, variant)
        self.client = AzureOpenAI(
            api_key=parameters.get("api_key", ""),
            api_version=parameters.get("api_version", ""),
            azure_endpoint=parameters.get("api_base", "")
        )
        self.chat_history = []

    def generate_response(self, prompt: str) -> str:
        logging.info(f"[AzureOpenAIGenerator] Prompt:\n{prompt}")

        self.chat_history.append({
            "role": "user",
            "content": prompt
        })

        try:
            response = self.client.chat.completions.create(
                model=self.parameters["deployment_name"],
                messages=self.chat_history,
                temperature=self.parameters["temperature"],
                max_tokens=self.parameters["max_tokens"]
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            logging.error(f"[AzureOpenAIGenerator] API call failed: {e}")
            raise

        logging.info(f"[AzureOpenAIGenerator] Response:\n{response_text}")

        self.chat_history.append({
            "role": "assistant",
            "content": response_text
        })

        logging.debug(f"[AzureOpenAIGenerator] Full Chat History:\n{self.chat_history}")

        return response_text

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "Azure OpenAI",
            "deployment": self.parameters["deployment_name"],
            "version": self.parameters["api_version"]
        }

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        base_params = super().get_init_parameters()
        azure_openai_params = {
            "api_key": {"type": "string", "description": "Azure OpenAI API key"},
            "api_base": {"type": "string", "description": "Azure OpenAI API base URL"},
            "api_type": {"type": "string", "description": "API type (usually 'azure')"},
            "api_version": {"type": "string", "description": "API version used by Azure OpenAI"},
            "deployment_name": {"type": "string", "description": "Azure OpenAI deployment name"},
            "temperature": {"type": "float", "description": "Controls randomness in output (0.0 - 1.0)"},
            "max_tokens": {"type": "int", "description": "Maximum number of tokens to generate"}
        }
        return {**base_params, **azure_openai_params}

    @classmethod
    def get_input_spec(cls) -> Dict[str, Dict[str, Any]]:
        return super().get_input_spec()

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        return super().get_output_spec()

