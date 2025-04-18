import time
from typing import Dict, Any, Type, Tuple

from app.models.chat import Chat
from app.models.components.AbstractComponent import AbstractComponent
from app.utils.helper import render_template


class WorkflowSystem:
    """
    A modular, pluggable RAG workflow built from components defined in a node-based config structure.
    """

    def __init__(self, wf_id: str, config: Dict[str, Any]):
        self.id = wf_id
        self.components: Dict[str, AbstractComponent] = {}
        self.edges: Dict[str, str] = {}

        nodes = config.get("nodes", [])
        if not nodes:
            raise ValueError("No nodes defined in the config.")

        for node_config in nodes:
            node_id = node_config["id"]
            type_string = node_config["type"]  # e.g., "generator/azure_openai/foo"
            path = type_string.split("/")

            variant_cls = self._resolve_component_path(path)

            component = variant_cls(
                id=node_id,
                name=node_config["name"],
                parameters=node_config.get("parameters", {}),
                variant=path[-1]
            )

            self.components[node_id] = component

        edges = config.get("edges", [])
        for edge in edges:
            source, target = edge["source"], edge["target"]

            if source in self.edges:
                raise ValueError(f"Multiple outgoing edges from node '{source}' are not supported")

            self.edges[source] = target

        print(edges)
        if "start" not in self.edges:
            raise ValueError("No 'start' node defined in edges.")
        if "end" not in self.edges.values():
            raise ValueError("No 'end' node defined in edges.")

        self.start_node, self.end_node = "start", "end"

    def generate_response(self, chat: Chat) -> Tuple[str, float]:
        """
        Generate a response from the generator component using the provided Chat object.
        """
        current_node = self.start_node
        data: Dict[str, Any] = {
            "chat": chat,
        }

        start_time = time.time()
        while True:
            component = self.components.get(current_node)
            if component is None:
                raise ValueError(f"Component '{current_node}' not found in workflow definition")
            data.update(component.execute(data))

            if current_node == self.end_node:
                break
            if current_node not in self.edges:
                raise ValueError(f"No outgoing edge found for node '{current_node}', and it's not the end node.")

            current_node = self.edges[current_node]

        end_time = time.time()

        if current_node != self.end_node:
            raise ValueError(f"Reached end component '{current_node}' which is not defined end '{self.end_node}'")
        else:
            response = render_template("f'{end.response}'", data)
            return response, float(end_time - start_time)  # TODO: see how to make this presentable in a useful way

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
