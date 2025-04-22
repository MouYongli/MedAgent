from app.models.components.AbstractComponent import AbstractComponent
from app.models.components.generator.Generator import Generator
from app.models.components.generator.AzureOpenAIGenerator import AzureOpenAIGenerator
from app.models.components.structure.EndComponent import EndComponent
from app.models.components.structure.StartComponent import StartComponent

Generator.variants = {
    "azure_openai": AzureOpenAIGenerator,
}

AbstractComponent.variants = {
    "generator": Generator,
    "start": StartComponent,
    "end": EndComponent,
}
