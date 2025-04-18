from app.models.components.AbstractComponent import AbstractComponent
from app.models.components.generator.Generator import Generator
from app.models.components.generator.AzureOpenAIGenerator import AzureOpenAIGenerator
from app.models.components.retriever.Retriever import Retriever
from app.models.components.retriever.VectorRetriever import VectorRetriever
from app.models.components.structure.EndComponent import EndComponent
from app.models.components.structure.StartComponent import StartComponent

Generator.variants = {
    "azure_openai": AzureOpenAIGenerator,
}

Retriever.variants = {
    "vector_weaviate": VectorRetriever,
}

AbstractComponent.variants = {
    "generator": Generator,
    "retriever": Retriever,
    "start": StartComponent,
    "end": EndComponent,
}
