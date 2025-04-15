from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
import copy

class AbstractComponent(ABC):
    variants: Dict[str, Type['AbstractComponent']] = {}
    default_parameters: Dict[str, Any] = {}

    @staticmethod
    def resolve_data_path(name: str, data: Dict[str, Any]) -> Any:
        """
        Resolves a dot-separated name like 'start.chat.current_user_input' from the given nested data dict.
        Works with dicts and object attributes.
        """
        parts = name.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict):
                if part not in current:
                    raise KeyError(f"Key '{part}' not found in dict at path: {'.'.join(parts)}")
                current = current[part]
            else:
                if not hasattr(current, part):
                    raise AttributeError(f"Attribute '{part}' not found in object at path: {'.'.join(parts)}")
                current = getattr(current, part)
        return current

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
    def get_input_spec(cls) -> Dict[str, Dict[str, Any]]:
        """
        Return a dictionary describing the expected inputs for the component.
        Each key is the input name, with metadata such as type and description.
        """
        return {}

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
