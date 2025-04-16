import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
import copy

class AbstractComponent(ABC):
    variants: Dict[str, Type['AbstractComponent']] = {}
    default_parameters: Dict[str, Any] = {}

    @staticmethod
    def resolve_template(template: str, context: dict):
        # TODO: UTILIZE IN COMPONENTS!!!
        template = template.strip()

        # Auto-detect f-string mode
        is_f_string = (
                (template.startswith("f'") and template.endswith("'")) or
                (template.startswith('f"') and template.endswith('"'))
        )

        if is_f_string:
            try:
                return eval(template, {}, context)
            except Exception as e:
                return f"<f-string error: {e}>"

        # Single expression inside {...}
        match = re.fullmatch(r"\{(.+?)\}", template)
        if match:
            expr = match.group(1)
            try:
                return eval(expr, {"__builtins__": __builtins__, "context": context}, context)
            except Exception as e:
                return f"<expression error: {e}>"

        return template  # Not an expression or f-string

    def __new__(cls, id: str, name: str, parameters: Optional[Dict[str, Any]] = None, variant: Optional[str] = None) -> 'AbstractComponent':
        if variant:
            if variant not in cls.variants:
                raise ValueError(f"Variant '{variant}' is not registered for component '{cls.__name__}'")
            subclass = cls.variants[variant]
            instance = super(AbstractComponent, subclass).__new__(subclass)
        else:
            if cls.variants:
                raise ValueError(
                    f"Component '{cls.__name__}' requires a variant. Available: {list(cls.variants.keys())}"
                )
            instance = super().__new__(cls)
        return instance

    def __init__(self, id: str, name: str, parameters: Optional[Dict[str, Any]] = None, variant: Optional[str] = None):
        self.id = id
        self.name = name
        self._variant = variant or "base"

        merged_params = copy.deepcopy(self.default_parameters)
        if parameters:
            merged_params.update(parameters)
        self.parameters = merged_params

    @classmethod
    def get_output_spec(cls) -> Dict[str, Dict[str, Any]]:
        """
        Return a dictionary describing the outputs provided by the component.
        Each key is the output name, with metadata such as type and description.
        """
        return {}

    @classmethod
    def get_init_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """
        Return a dictionary describing the parameters for the component.
        Each key is the parameter name, with metadata such as type and description.
        """
        return {}

    @classmethod
    def register_variant(cls, name: str, variant_cls: Type['AbstractComponent']):
        cls.variants[name] = variant_cls

    def __init_subclass__(cls, variant_name: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if variant_name:
            AbstractComponent.variants[variant_name] = cls

    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def get_variant_name(self) -> str:
        return self._variant
