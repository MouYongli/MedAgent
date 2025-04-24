from typing import List

from openai import AzureOpenAI


class OpenAIEmbedder:
    def __init__(self, api_key: str, api_base: str, api_version: str, deployment_name: str):
        self.deployment_name = deployment_name
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base
        )

    def embed(self, text: str) -> List[float]:
        text = text.replace("\n", " ")  # recommended normalization
        response = self.client.embeddings.create(
            input=[text],
            model=self.deployment_name  # using Azure deployment name as model reference
        )
        return response.data[0].embedding
