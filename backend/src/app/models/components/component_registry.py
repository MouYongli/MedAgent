from app.models.components.AbstractComponent import AbstractComponent
from app.models.components.generator.Generator import Generator
from app.models.components.generator.AzureOpenAIGenerator import AzureOpenAIGenerator

Generator.variants = {
    "azure_openai": AzureOpenAIGenerator,
}

AbstractComponent.variants = {
    "generator": Generator,
}
