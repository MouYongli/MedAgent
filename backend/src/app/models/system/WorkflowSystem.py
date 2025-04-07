import uuid
from typing import Dict, Any, Type
from app.models.components.AbstractComponent import AbstractComponent
from app.models.components.generator.Generator import Generator
from app.models.chat import Chat


class WorkflowSystem:
    """
    A modular, pluggable RAG workflow built from components defined in a node-based config structure.
    """

    def __init__(self, config: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.components: Dict[str, AbstractComponent] = {}

        nodes = config.get("nodes", {})
        if not nodes:
            raise ValueError("No nodes defined in the config.")

        for node_id, node_config in nodes.items():
            type_string = node_config["type"]  # e.g., "generator/azure_openai/foo"
            path = type_string.split("/")

            variant_cls = self._resolve_component_path(path)

            component = variant_cls(
                name=node_config["name"],
                inputs=node_config.get("inputs", {}),
                outputs=node_config.get("outputs", {}),
                parameters=node_config.get("parameters", {}),
                variant=path[-1]
            )

            self.components[node_id] = component

    def generate_response(self, chat: Chat) -> str:
        """
        Generate a response from the generator component using the provided Chat object.
        """
        generator_component = self.components.get("generator")
        if not isinstance(generator_component, Generator):
            raise ValueError("No valid 'generator' node of type Generator found.")
        return generator_component.generate_response(chat)

    def _resolve_component_path(self, path: list[str]) -> Type[AbstractComponent]:
        """
        Resolves a component path like ['generator', 'azure_openai', 'foo']
        by walking through nested .variants dictionaries.
        """
        current_cls = self._resolve_base_class(path[0])
        for variant_name in path[1:]:
            if not hasattr(current_cls, "variants") or not isinstance(current_cls.variants, dict):
                raise TypeError(f"'{current_cls.__name__}' must define a 'variants' dictionary.")
            if variant_name not in current_cls.variants:
                raise ValueError(f"Variant '{variant_name}' not found in '{current_cls.__name__}'. "
                                 f"Available: {list(current_cls.variants.keys())}")
            current_cls = current_cls.variants[variant_name]
        return current_cls

    def _resolve_base_class(self, base_type: str) -> Type[AbstractComponent]:
        if base_type not in AbstractComponent.variants:
            raise ValueError(f"No base component class found for '{base_type}'")
        return AbstractComponent.variants[base_type]

